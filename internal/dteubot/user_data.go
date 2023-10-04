package dteubot

import (
	"github.com/cubicbyte/dteubot/internal/db"
	"time"
)

type UserDataManager struct {
	UserId int64
}

type UserData struct {
	UserId    int64     `db:"user_id"`
	FirstName string    `db:"first_name"`
	Username  string    `db:"username"`
	IsAdmin   bool      `db:"is_admin"`
	Referral  string    `db:"referral"`
	Created   time.Time `db:"created"`
}

func (m *UserDataManager) GetUserData() (*UserData, error) {
	log.Debugf("Getting user data for user %d\n", m.UserId)

	userData := new(UserData)
	err := Database.Db.Get(userData, db.GetUserQuery, m.UserId)
	if err != nil {
		return nil, err
	}

	return userData, nil
}

func (m *UserDataManager) UpdateUserData(userData *UserData) error {
	log.Debugf("Updating user data for user %d\n", userData.UserId)

	_, err := Database.Db.NamedExec(db.UpdateUserQuery, userData)
	if err != nil {
		return err
	}

	return nil
}

func (m *UserDataManager) CreateUserData(firstName string, username *string, referral *string) error {
	log.Debugf("Creating user data for user %d\n", m.UserId)

	_, err := Database.Db.Exec(db.CreateUserQuery, m.UserId, firstName, username, referral)
	if err != nil {
		return err
	}

	return nil
}

func (m *UserDataManager) IsUserExists() (bool, error) {
	log.Debugf("Checking if user %d exists\n", m.UserId)

	var exists bool
	err := Database.Db.Get(&exists, db.IsUserExistsQuery, m.UserId)
	if err != nil {
		return false, err
	}

	return exists, nil
}
