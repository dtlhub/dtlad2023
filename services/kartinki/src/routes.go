package main

import (
	"fmt"
	"log"
	"net/http"
	"strconv"

	"github.com/YellowPhil/pwnAD/controllers"
	"github.com/gin-gonic/gin"
)

func authenticateUser(c *gin.Context, id uint, sessionToken string) {
	c.SetCookie("token", sessionToken, 3600, "/", "localhost", false, true)
	c.SetCookie("userID", fmt.Sprintf("%v", id), 3600, "/", "", false, true)
	c.Set("logged_in", true)
}

func deauthenticateUser(c *gin.Context) {
	c.SetCookie("token", "", -1, "/", "localhost", false, true)
	c.Set("logged_in", false)
}

func showMainPage(g *gin.Context) {
	var results []controllers.LabResult
	results = labController.GetLabs()
	render(g, "index.html", gin.H{"header": "Home page", "payload": results})
}

func showRegisterPage(c *gin.Context) {
	render(c, "register.html", gin.H{"title": "Register"})
}

func RegisterNewUser(c *gin.Context) {
	username := c.PostForm("username")
	password := c.PostForm("password")

	if err := userController.RegisterUser(username, password); err != nil {
		c.HTML(http.StatusBadRequest, "register.html", gin.H{
			"ErrorTitle":   "Registration failed",
			"ErrorMessage": "Username already taken",
		})
		return
	}
	render(c, "registration-successful.html", gin.H{"title": "Registered successfully"})
}

func showLoginPage(c *gin.Context) {
	render(c, "login.html", gin.H{"title": "Login"})
}

func LoginUser(c *gin.Context) {
	username := c.PostForm("username")
	password := c.PostForm("password")

	id, token, err := userController.CheckLoginUser(username, password)
	if err != nil {
		log.Println(err)
		c.HTML(http.StatusBadRequest, "login.html", gin.H{
			"ErrorTitle":   "Login Failed",
			"ErrorMessage": "Invalid credentials provided"})
		return
	}

	authenticateUser(c, id, token)
	render(c, "login-successful.html", gin.H{"title": "Login successful"})
}

func LogoutUser(c *gin.Context) {
	deauthenticateUser(c)
	showMainPage(c)
}

func showLabsPage(c *gin.Context) {
	id, _ := c.Cookie("userID")
	userID, _ := strconv.Atoi(id)
	labs := labController.GetUserLabs(uint(userID))
	render(c, "labs.html", gin.H{"payload": labs})
}

func showAddLabPage(c *gin.Context) {

}

func AddLab(c *gin.Context) {
}

func testRoute(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{"Well!": "Done!"})
}
