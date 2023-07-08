package controllers

import (
	"errors"
	"math"

	"gorm.io/gorm"
)

const measurements = 10
const studentsCoefficient = 201
const eps = 0.01

type LabResult struct {
	gorm.Model
	Error      float64 `json:"eps"`
	Expected   float64 `json:"expected"`
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

func newLabResult(expected, testResult float64, comment string) *LabResult {
	lr := &LabResult{
		Expected:   expected,
		TestResult: testResult,
		Comment:    comment,
	}
	lr.calculateMeasurementError(expected, testResult)
	return lr
}

func (lc *LabResultsController) GetLabs() []LabResult {
	var results []LabResult
	lc.db.Find(&results)
	return results
}

func (lc *LabResultsController) GetUserLabs(id uint) []LabResult {
	var (
		tmp    []LabResult
		nigger []LabResult
		user   User
		result []LabResult
	)
	lc.db.First(&user, id)
	lc.db.Model(user).Association("Labs").Find(&tmp)

	// return all labs that are withing the small Error range
	for _, res := range tmp {
		lc.db.Model(&LabResult{}).Where("expected BETWEEN ? AND ?", res.Expected-eps, res.Expected+eps).Find(&result)
		nigger = append(nigger, result...)
	}
	return nigger
}

func (lc *LabResultsController) AddNewLabResult(userID uint, expectedResult, testResult float64, comment string) error {
	var user User

	if math.Abs(expectedResult-testResult) < 100000 {
		return errors.New("Student is cheating)")
	}
	newLab := newLabResult(expectedResult, testResult, comment)
	lc.db.First(&user, userID)
	return lc.db.Model(&user).Association("Labs").Append(newLab)

}
