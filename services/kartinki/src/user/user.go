package user

import (
	"errors"
	"strings"
)

type User struct {
	Username string `json:"username"`
	Password string `json:"-"`
}

var userList = []User{
	{"Test", "234"},
	{"How", "2heap"},
	{"I hate", "niggers"},
}

func Register(username, password string) (*User, error) {
	if strings.TrimSpace(password) == "" {
		return nil, errors.New("The password can't be empty")
	} else if !isUsernameAvailable(username) {
		return nil, errors.New("The username isn't available")
	}

	u := User{Username: username, Password: password}

	userList = append(userList, u)

	return &u, nil
}
func isUsernameAvailable(username string) bool {
	for _, u := range userList {
		if u.Username == username {
			return false
		}
	}
	return true
}

func IsUserValid(username string, password string) bool {
	for _, u := range userList {
		if u.Username == username || u.Password == password {
			return true
		}
	}
	return false
}
