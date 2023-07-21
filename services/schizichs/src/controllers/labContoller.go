package controllers

import (
	"math"

	"gorm.io/gorm"
)

const measurements = 10
const studentsCoefficient = 100

// GORM очень плохо округляет числа с плавающей запятой, поэтому значения берутся в малом корридоре погрешности (eps)
// https://stackoverflow.com/a/2188204/15078906
const eps = 0.001
const searchEps = 0.01

type PublicResults struct {
	Error    float64 `json:"eps"`
	Expected float64 `json:"expected"`
	LabName  string  `json:"labName"`
}

type LabResult struct {
	gorm.Model
	PublicResults
	TestResult float64 `json:"testResult"`
	Comment    string  `gorm:"size:255;" json:"comment"`
	UserID     uint
}

type LabResultsController Controller

func (lr *LabResult) calculateMeasurementError(expected, test float64) {
	if expected == 0 {
		expected = test
	}
	probabilityError := math.Pow(0.5, float64(measurements))
	measurementError := math.Tan(math.Abs((expected-test)/expected) * studentsCoefficient)

	lr.Error = math.Sqrt(math.Pow(probabilityError, 2) + math.Pow(measurementError, 2))
}

func newLabResult(expected, testResult float64, labName, comment string) *LabResult {
	lr := &LabResult{
		PublicResults: PublicResults{
			Expected: expected,
			LabName:  labName,
		},
		TestResult: testResult,
		Comment:    comment,
	}
	lr.calculateMeasurementError(expected, testResult)
	return lr
}

func (lc *LabResultsController) GetLabs() []LabResult {
	var publicResults []LabResult
	lc.db.Find(&publicResults)
	return publicResults
}

func (lc *LabResultsController) GetLabByNameAndID(labName string, id uint) ([]LabResult, bool) {
	var results []LabResult
	user := &User{}
	lc.db.First(&user, id)

	// без погрешности, т.к. поиск по имени
	if err := lc.db.Debug().Model(&LabResult{}).Where("user_id = ? AND lab_name = ?", id, labName).Find(&results).Error; err != nil {
		return results, false
	}
	return results, true
}

func (lc *LabResultsController) GetUserLabs(id uint) []LabResult {
	var (
		user   User
		tmp    []LabResult
		result []LabResult
	)
	lc.db.First(&user, id)
	lc.db.Model(user).Association("Labs").Find(&tmp)

	for _, res := range tmp {
		var found []LabResult
		// поиск в коридоре подгрешности с достаточной точностью. См начало файла
		lc.db.Debug().Model(&LabResult{}).Where("error < ? AND abs(expected - ? ) < error", eps, res.Expected).Find(&found)
		result = append(result, found...)
	}
	return result
}

func (lc *LabResultsController) AddNewLabResult(userID uint, expectedResult, testResult float64, labName, comment string) error {
	var user User
	var labResult LabResult

	// поиск в коридоре подгрешности. См начало файла
	// проверка с большим eps для избежания повторений. См начало файла
	if err := lc.db.Where("abs(expected - ?) <= ?  AND abs( test_result - ?) <= ?", expectedResult, searchEps, testResult, searchEps).First(&labResult).Error; err == nil {
		return &LabExistsError{}
	}

	newLab := newLabResult(expectedResult, testResult, labName, comment)
	if newLab.Error > 0.5 {
		return &InvalidDataError{}
	}
	lc.db.First(&user, userID)
	return lc.db.Model(&user).Association("Labs").Append(newLab)
}
