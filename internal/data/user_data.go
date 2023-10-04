package data

import (
	"time"
)

// UserDataManager makes it easier to work with user data.
type UserDataManager struct {
	UserId int64
}

// UserData is a struct that contains all the data about a user.
type UserData struct {
	UserId    int64     `db:"user_id"`
	FirstName string    `db:"first_name"`
	Username  string    `db:"username"`
	IsAdmin   bool      `db:"is_admin"`
	Referral  string    `db:"referral"`
	Created   time.Time `db:"created"`
}

// GetUserData returns user data for the user.
func (m *UserDataManager) GetUserData() (*UserData, error) {
	log.Debugf("Getting user data for user %d\n", m.UserId)

	userData := new(UserData)
	err := DbInstance.Db.Get(userData, GetUserQuery, m.UserId)
	if err != nil {
		return nil, err
	}

	return userData, nil
}

// UpdateUserData updates user data for the user.
func (m *UserDataManager) UpdateUserData(userData *UserData) error {
	log.Debugf("Updating user data for user %d\n", userData.UserId)

	_, err := DbInstance.Db.NamedExec(UpdateUserQuery, userData)
	if err != nil {
		return err
	}

	return nil
}

// CreateUserData creates user data for the user.
func (m *UserDataManager) CreateUserData() (*UserData, error) {
	log.Debugf("Creating user data for user %d\n", m.UserId)

	userData := new(UserData)
	err := DbInstance.Db.Get(userData, CreateUserQuery, m.UserId)
	if err != nil {
		return nil, err
	}

	return userData, nil
}

// IsUserExists checks if the user exists in the database.
func (m *UserDataManager) IsUserExists() (bool, error) {
	log.Debugf("Checking if user %d exists\n", m.UserId)

	var exists bool
	err := DbInstance.Db.Get(&exists, IsUserExistsQuery, m.UserId)
	if err != nil {
		return false, err
	}

	return exists, nil
}

// GetOrCreateUserData returns user data for the user or creates it if it doesn't exist.
func (m *UserDataManager) GetOrCreateUserData() (*UserData, error) {
	// Check if user data exists
	exists, err := m.IsUserExists()
	if err != nil {
		return nil, err
	}

	// If user data doesn't exist, create it
	if !exists {
		userData, err := m.CreateUserData()
		if err != nil {
			return nil, err
		}
		return userData, nil
	}

	// Get user data
	userData, err := m.GetUserData()
	if err != nil {
		return nil, err
	}

	return userData, nil
}
