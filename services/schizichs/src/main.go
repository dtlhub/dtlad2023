package main

import (
	"net/http"

	"github.com/YellowPhil/pwnAD/controllers"
	"github.com/gin-gonic/gin"
)

var router *gin.Engine

var userController *controllers.UserController
var labController *controllers.LabResultsController

func initRoutes() {
	router.GET("/", showMainPage)

	userRoutes := router.Group("/user")
	{
		userRoutes.GET("/register", showRegisterPage)
		userRoutes.POST("/register", RegisterNewUser)
		userRoutes.GET("/login", showLoginPage)
		userRoutes.POST("/login", LoginUser)
		userRoutes.GET("/logout", AuthMiddleWare(), LogoutUser)
	}
	labsRoute := router.Group("/labs").Use(AuthMiddleWare())
	{
		labsRoute.GET("/show", showLabsPage)
		labsRoute.GET("/new", showAddLabPage)
		labsRoute.POST("/new", AddLab)

	}
}

func main() {
	router = gin.Default()
	router.LoadHTMLGlob("templates/*")

	db, _ := controllers.Setup()
	labController, userController = controllers.SetupControllers(db)

	initRoutes()
	router.Run()
}

func render(c *gin.Context, templateName string, data gin.H) {
	if token, err := c.Cookie("token"); err == nil && token != "" {
		data["Authorized"] = true
	} else {
		data["Authorized"] = false
	}
	switch c.Request.Header.Get("Accept") {
	case "application/json":
		c.JSON(http.StatusOK, data["payload"])
	case "application/xml":
		c.XML(http.StatusOK, data["payload"])
	default:
		c.HTML(http.StatusOK, templateName, data)
	}
}
