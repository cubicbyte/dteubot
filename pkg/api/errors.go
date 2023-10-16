/*
 * Copyright (c) 2022 Bohdan Marukhnenko
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

package api

import "errors"

// HTTPApiError is an error returned by the API when status code is not 200
type HTTPApiError struct {
	Code int
	Body string
	Err  error
}

// InternalServerError is an error returned by the API when status code is 500
type InternalServerError struct {
	Name    string `json:"name"`
	Message string `json:"message"`
	Code    int    `json:"code"`
	Status  int    `json:"status"`
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

func (e *InternalServerError) Error() string {
	return errors.New("internal server error").Error()
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
