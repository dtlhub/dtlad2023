package controllers

import (
	"errors"
	"math"

	"gorm.io/gorm"
)

const measurements = 10
const studentsCoefficient = 100
const eps = 0.1

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
	lc.db.Model(user).Association("Labs").Find(&result)

	// return all labs that are withing the small Error range
	for _, res := range tmp {
		lc.db.Debug().Model(&LabResult{}).Where("expected = ? AND error <= ?", res.Expected, eps).Find(&tmp)
		result = append(result, tmp...)
	}
	return result
}

func (lc *LabResultsController) AddNewLabResult(userID uint, expectedResult, testResult float64, labName, comment string) error {
	var user User

	if math.Abs(expectedResult-testResult) < 100000 {
		return errors.New("Student is cheating)")
	}
	newLab := newLabResult(expectedResult, testResult, labName, comment)
	lc.db.First(&user, userID)
	return lc.db.Model(&user).Association("Labs").Append(newLab)
}