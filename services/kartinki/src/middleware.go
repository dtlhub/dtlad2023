package main

import (
	"github.com/YellowPhil/pwnAD/controllers"
	"github.com/gin-gonic/gin"
)

func AuthMiddleWare() gin.HandlerFunc {
	return func(c *gin.Context) {
		tokenString, err := c.Cookie("token")
		if err != nil || tokenString == "" {
			c.AbortWithStatusJSON(401, gin.H{"Error": "No JWT token provided"})
			return
		}
		if err := controllers.ValidateToken(tokenString); err != nil {
			c.AbortWithStatusJSON(401, gin.H{"Error": "Not a valid JWT token"})
		}
	}
}
