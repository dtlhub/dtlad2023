package controllers

import (
	"errors"
	"time"

	"github.com/golang-jwt/jwt/v4"
)

const key = "SEСREТ_KEY"

type JWTClaim struct {
	Id         uint `json:"username"`
	Authorized bool `json:"authorized"`
	jwt.StandardClaims
}

func GenerateToken(user *User) (string, error) {
	expirationTime := time.Now().Add(1 * time.Hour)
	claims := &JWTClaim{Id: user.ID, Authorized: true,
		StandardClaims: jwt.StandardClaims{
			ExpiresAt: expirationTime.Unix(),
		}}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString([]byte(key))
}

func ValidateToken(signedToken string, id uint) (err error) {
	token, err := jwt.ParseWithClaims(
		signedToken,
		&JWTClaim{},
		func(token *jwt.Token) (interface{}, error) {
			return []byte(key), nil
		},
	)
	if err != nil {
		return err
	}

	claims, ok := token.Claims.(*JWTClaim)
	if !ok {
		return errors.New("couldn't parse claims")
	}

	if claims.ExpiresAt < time.Now().Local().Unix() {
		return errors.New("token expired")
	}

	if claims.Id != id || claims.Authorized != true {
		return errors.New("Invalid token")
	}
	return nil
}
