package main

import (
	"fmt"
	"log"
	"net/http"
	"strconv"
	"github.com/YellowPhil/pwnAD/controllers"
in-gonic/gin"
)

type userData struct {
	Username string `form:"username" json:"username" binding:"required"`
	Password string `form:"username" json:"password" binding:"required"`
}

type labData struct {
	LabName        string  `form:"labName" json:"labName" binding:"required"`
	TestResult     float64 `form:"testResult" json:"testResult" binding:"required,numeric"`
	ExpectedResult float64 `form:"expectedResult" json:"expectedResult" binding:"required,numeric"`
	Comment        string  `form:"comment" json:"comment" binding:"required"`
}

func authenticateUser(c *gin.Context, id uint, sessionToken string) {
	c.SetCookie("token", sessionToken, 3600, "/", "localhost:8080", false, true)
	c.SetCookie("userID", fmt.Sprintf("%v", id), 3600, "/", "", false, true)
	c.Set("userID", id)
}

func deauthenticateUser(c *gin.Context) {
	c.SetCookie("token", "", 100, "/", "", false, true)
	c.SetCookie("userID", "", 100, "/", "", false, true)
}

func showMainPage(g *gin.Context) {
	publicResults := labController.GetLabs()
	render(g, "index.html", gin.H{"header": "Home page", "publicResults": publicResults})
}

func showRegisterPage(c *gin.Context) {
	render(c, "register.html", gin.H{"title": "Register"})
}

func RegisterNewUser(c *gin.Context) {
	newUserData := userData{}
	if err := c.ShouldBind(&newUserData); err != nil {
		c.AbortWithStatusJSON(http.StatusBadRequest, gin.H{
			"Error": "not a valid user data",
		})
		return
	}

	id, token, err := userController.RegisterUser(newUserData.Username, newUserData.Password)
	if err != nil {
		c.HTML(http.StatusBadRequest, "register.html", gin.H{
			"ErrorTitle":   "Registration failed",
			"ErrorMessage": "Username already taken",
		})
		return
	}
	authenticateUser(c, id, token)
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
	c.Redirect(http.StatusMovedPermanently, "/")
}

func showLabsPage(c *gin.Context) {
	id, _ := c.Cookie("userID")
	userID, _ := strconv.Atoi(id)
	labs := labController.GetUserLabs(uint(userID))
	if labName, ok := c.GetQuery("labname"); ok {
		showSingleLabPage(c, uint(userID), labName)
		return
	}
	render(c, "labs.html", gin.H{"title": "your labs", "payload": labs})
}

func showSingleLabPage(c *gin.Context, userID uint, labName string) {
	if labs, ok := labController.GetLabByNameAndID(labName, userID); ok {
		render(c, "labs.html", gin.H{"title": "Labs with name" + labName, "payload": labs})
	} else {
		c.AbortWithStatusJSON(http.StatusBadRequest, gin.H{"Error": "No such lab"})
	}
}

func showAddLabPage(c *gin.Context) {
	id, _ := c.Cookie("userID")
	userID, _ := strconv.Atoi(id)
	user, err := userController.GetUserByID(uint(userID))
	if err != nil {
		c.AbortWithError(http.StatusBadRequest, err)
	}
	render(c, "input-lab.html", gin.H{"title": "Add lab", "Username": user.Username})
}

func AddLab(c *gin.Context) {
	newLabData := labData{}
	if err := c.ShouldBind(&newLabData); err != nil {
		c.AbortWithStatusJSON(http.StatusBadRequest, gin.H{"Error": "Not a valid lab data"})
		return
	}
	id, _ := c.Cookie("userID")
	userID, _ := strconv.Atoi(id)

	err := labController.AddNewLabResult(uint(userID), newLabData.ExpectedResult, newLabData.TestResult, newLabData.LabName, newLabData.Comment)
	switch err.(type) {
	case *controllers.InvalidDataError:
		c.HTML(http.StatusBadRequest, "input-lab.html", gin.H{
			"ErrorTitle":   "Пересчитывай!",
			"ErrorMessage": "Погрешность в лабораторной слишком велика",
		})
	case *controllers.LabExistsError:
		c.HTML(http.StatusBadRequest, "input-lab.html", gin.H{
			"ErrorTitle":   "Не списывать!",
			"ErrorMessage": "Такая лабораторная уже есть",
		})
	default:
		c.Redirect(http.StatusMovedPermanently, "/labs/show")
	}
}
