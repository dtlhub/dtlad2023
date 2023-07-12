package main

import (
	"fmt"
	"strconv"

	"github.com/YellowPhil/pwnAD/controllers"
	"github.com/gin-gonic/gin"
)

func AuthMiddleWare() gin.HandlerFunc {
	return func(c *gin.Context) {
		tokenString, err := c.Cookie("token")
		if err != nil {
			c.AbortWithStatusJSON(403, gin.H{"Error": "No jwt provided"})
			return
		}
		if id, err := (c.Cookie("userID")); err == nil {
			userID, err := strconv.Atoi(id)
			if err != nil {
				fmt.Println(err)
				c.AbortWithStatusJSON(403, gin.H{"Error": "Invalid userID cookie"})
				return
			}
			if err := controllers.ValidateToken(tokenString, uint(userID)); err != nil {
				fmt.Println(err)
				c.AbortWithStatusJSON(403, gin.H{"Error": "Invalid JWT"})
				return
			}
		} else {
			fmt.Println(err)
			c.AbortWithStatusJSON(43, gin.H{"Error": "No userID cookie provided"})
			return
		}
		c.Next()
	}
}
