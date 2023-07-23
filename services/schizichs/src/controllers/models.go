package controllers

type LabExistsError struct {
	msg string
}

func (e *LabExistsError) Error() string { return e.msg }

type InvalidDataError struct {
	msg string
}

func (e *InvalidDataError) Error() string { return e.msg }
