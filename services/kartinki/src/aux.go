package main

import (
	"math/rand"
	"strconv"

	"github.com/gin-gonic/gin"
)

func generateSessionToken() string {
	return strconv.FormatInt(rand.Int63(), 16)
}

func authenticateUser(c *gin.Context, sessionToken string) {

	c.SetCookie("token", sessionToken, 3600, "/", "", false, true)
	c.Set("logged_in", true)
}

func deauthenticateUser(c *gin.Context) {
	c.SetCookie("token", "", -1, "/", "", false, true)
	c.Set("logged_int", false)
}
