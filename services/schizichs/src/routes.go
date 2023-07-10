package main

import (
	"fmt"
	"log"
	"net/http"
	"strconv"

	"github.com/YellowPhil/pwnAD/controllers"
	"github.com/gin-gonic/gin"
)

type userData struct {
	Username string `form:"username" json:"username" binding:"required"`
	Password string `form:"username" json:"password" binding:"required"`
}

type labData struct {
	TestResult     float64 `form:"testResult" json:"testResult" binding:"required,numeric"`
	ExpectedResult float64 `form:"expectedResult" json:"expectedResult" binding:"required,numeric"`
	Comment        string  `form:"comment" json:"comment"`
}

func authenticateUser(c *gin.Context, id uint, sessionToken string) {
	c.SetCookie("token", sessionToken, 3600, "/", "localhost:8080", false, true)
	c.SetCookie("userID", fmt.Sprintf("%v", id), 3600, "/", "", false, true)
	c.Set("userID", id)
}

func deauthenticateUser(c *gin.Context) {
	c.SetCookie("token", "goldTrigger", 100, "/", "localhost:8080", false, true)
	c.SetCookie("userID", "-1", 100, "/", "localhost:8080", false, true)
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
	newUserData := userData{}
	if err := c.ShouldBind(&newUserData); err != nil {
		c.HTML(http.StatusBadRequest, "register.html", gin.H{
			"ErrorTitle":   "Registration failed",
			"ErrorMessage": "Not a valid user data",
		})
		return
	}
	//	username := c.PostForm("username")
	//	password := c.PostForm("password")
	//
	if err := userController.RegisterUser(newUserData.Username, newUserData.Password); err != nil {
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
	newUserData := userData{}

	if err := c.ShouldBind(&newUserData); err != nil {
		c.AbortWithStatusJSON(http.StatusBadRequest, gin.H{"Error": "Not a valid user data"})
		return
	}
	id, token, err := userController.CheckLoginUser(newUserData.Username, newUserData.Password)
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
	c.JSON(200, gin.H{"NIGGEr": "DALE"})
}

func showLabsPage(c *gin.Context) {
	id, _ := c.Cookie("userID")
	userID, _ := strconv.Atoi(id)
	labs := labController.GetUserLabs(uint(userID))
	render(c, "labs.html", gin.H{"payload": labs})
}

func showAddLabPage(c *gin.Context) {
	id, _ := c.Cookie("userID")
	userID, _ := strconv.Atoi(id)
	user, err := userController.GetUserByID(uint(userID))
	if err != nil {
		c.AbortWithError(http.StatusBadRequest, err)
	}
	render(c, "input-lab.html", gin.H{"title": "Add lab", "user": user})
}

func AddLab(c *gin.Context) {
	newLabData := labData{}
	if err := c.ShouldBind(&newLabData); err != nil {
		c.AbortWithStatusJSON(http.StatusBadRequest, gin.H{"Error": "Not a valid lab data"})
		return
	}
	id, _ := c.Cookie("userID")
	userID, _ := strconv.Atoi(id)

	if err := labController.AddNewLabResult(uint(userID), newLabData.TestResult, newLabData.ExpectedResult, newLabData.Comment); err != nil {
		c.HTML(http.StatusBadRequest, "input-lab.html", gin.H{
			"ErrorTitle":   "Не списывать!",
			"ErrorMessage": "Теоретические данные слишком похожи на практику",
		})
		return
	}
	c.Redirect(http.StatusMovedPermanently, "/labs/show")
}
