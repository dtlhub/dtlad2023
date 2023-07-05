package controllers

import (
	"fmt"
	"html"
	"strings"

	"golang.org/x/crypto/bcrypt"
	"gorm.io/gorm"
)

type User struct {
	gorm.Model
	Username string      `gorm:"size:255;not null;unique" json:"username"`
	Password string      `gorm:"size:255;not null;" json:"-"`
	Labs     []LabResult `gorm:"foreignKey:UserID"`
}

func (user *User) HashPassword() error {
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(user.Password), bcrypt.DefaultCost)
	if err != nil {
		return err
	}
	user.Password = string(hashedPassword)
	user.Username = html.EscapeString(strings.TrimSpace(user.Username))
	return nil
}

func verifyPassword(hashedPassword, providedPassword string) error {
	return bcrypt.CompareHashAndPassword([]byte(hashedPassword), []byte(providedPassword))
}

type UserController Controller

func (c *UserController) RegisterUser(username, password string) error {
	NewUser := &User{Username: username, Password: password}
	NewUser.HashPassword()

	if err := c.db.Create(NewUser).Error; err != nil {
		return err
	}
	return nil
}

func (c *UserController) CheckLoginUser(username, password string) (uint, string, error) {
	user := &User{}
	if err := c.db.Model(user).Where("username = ?", username).Take(user).Error; err != nil {
		return 0, "", err
	}
	if err := verifyPassword(user.Password, password); err != nil && err == bcrypt.ErrMismatchedHashAndPassword {
		return 0, "", fmt.Errorf("Invalid password for user %s", username)
	}
	token, err := GenerateToken(user)
	if err != nil {
		return 0, "", err
	}
	return user.ID, token, nil
}

func (c *UserController) GetUserByID(id uint) (*User, error) {
	user := &User{}
	if err := c.db.First(user, id).Error; err != nil {
		return nil, err
	}
	return user, nil
}
