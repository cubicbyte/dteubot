package api

import "errors"

// HTTPApiError is an error returned by the API when status code is not 200
type HTTPApiError struct {
	Code int
	Body string
}

// UnauthorizedError is an error returned by the API when status code is 401
type UnauthorizedError struct {
	Name    string `json:"name"`
	Message string `json:"message"`
	Code    int    `json:"code"`
	Status  int    `json:"status"`
}

// ForbiddenError is an error returned by the API when status code is 403
type ForbiddenError struct {
	Name    string `json:"name"`
	Message string `json:"message"`
	Code    int    `json:"code"`
	Status  int    `json:"status"`
}

// ValidationError is an error returned by the API when status code is 422.
// It means that the request body is invalid
type ValidationError struct {
	Fields []ValidationErrorField `json:"fields"`
}

// ValidationErrorField is a field of ValidationError
type ValidationErrorField struct {
	Field   string `json:"field"`
	Message string `json:"message"`
}

func (e *HTTPApiError) Error() string {
	return errors.New("api error").Error()
}

func (e *UnauthorizedError) Error() string {
	return errors.New("unauthorized").Error()
}

func (e *ForbiddenError) Error() string {
	return errors.New("forbidden").Error()
}

func (e *ValidationError) Error() string {
	return errors.New("validation error").Error()
}
