package main

import (
	"errors"
	"fmt"
	"strconv"

	"github.com/YellowPhil/pwnAD/controllers"
	"github.com/gin-gonic/gin"
)

func AuthMiddleWare() gin.HandlerFunc {
	return func(c *gin.Context) {
		tokenString, err := c.Cookie("token")
		if err != nil {
			c.AbortWithError(403, errors.New("No JWT token provided"))
			return
		}
		if id, err := (c.Cookie("userID")); err == nil {
			userID, err := strconv.Atoi(id)
			if err != nil {
				fmt.Println(err)
				c.AbortWithStatus(403)
				return
			}
			if err := controllers.ValidateToken(tokenString, uint(userID)); err != nil {
				fmt.Println(err)
				c.AbortWithStatus(403)
				return
			}
		} else {
			fmt.Println(err)
			c.AbortWithStatus(403)
			return
		}
		c.Next()
	}
}
