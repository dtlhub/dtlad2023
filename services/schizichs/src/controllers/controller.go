package controllers

import (
	"errors"
	"fmt"

	"golang.org/x/crypto/bcrypt"
	"gorm.io/gorm"
)

type Controller struct {
	db *gorm.DB
}

func (c *Controller) RegisterUser(username, password string) error {
	NewUser := &User{Username: username, Password: password}
	NewUser.HashPassword()

	if err := c.db.Create(NewUser).Error; err != nil {
		return errors.New("Could not register user")
	}
	return nil
}

func (c *Controller) CheckLoginUser(username, password string) (string, error) {
	user := &User{}

	if err := c.db.Model(User{}).Where("username = ?", username).Take(user).Error; err != nil {
		return "", err
	}

	if err := verifyPassword(user.Password, password); err != nil && err == bcrypt.ErrMismatchedHashAndPassword {
		return "", fmt.Errorf("Invalid password for user %s", username)
	}

	token, err := GenerateToken(user)
	if err != nil {
		return "", err
	}

	return token, nil
}
