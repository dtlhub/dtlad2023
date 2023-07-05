package controllers

import (
	"fmt"
	"math"

	"gorm.io/gorm"
)

type LabResult struct {
	gorm.Model
	Error      float64 `json:"eps"`
	Expected   float32 `json:"expected"`
	TestResult float32 `json:"testResult"`
	Comment    string  `json:"comment"`
	UserID     uint
}

type LabResultsController Controller

func (lr *LabResult) calculateMeasurementError(expected, test float32) {
	if expected == 0 {
		expected = test
	}
	measurements := 10
	probabilityError := 1 - math.Pow(0.5, float64(measurements))
	studentsCoefficient := 0.13

	measurementError := (expected - test/expected) * float32(studentsCoefficient)

	lr.Error = math.Sqrt(math.Pow(float64(measurementError), 2) + math.Pow(probabilityError, 2))

}

func newLabResult(expected, testResult float32, comment string) *LabResult {
	lr := &LabResult{
		Expected:   expected,
		TestResult: testResult,
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
	var result []LabResult
	var user User
	lc.db.First(&user, id)
	lc.db.Model(user).Association("Labs").Find(&result)
	for _, v := range result {
		fmt.Println(v)
	}
	return result
}

func (lc *LabResultsController) AddNewLabResult(userID uint, expectedResult, testResult float32, comment string) error {
	var user User
	newLab := newLabResult(expectedResult, testResult, comment)
	lc.db.First(&user, userID)
	return lc.db.Model(&user).Association("Labs").Append(newLab)

}
