package main

import (
	"net/http"

	"github.com/YellowPhil/pwnAD/controllers"
	"github.com/YellowPhil/pwnAD/public"
	"github.com/gin-gonic/gin"
)

var router *gin.Engine

var gallery []public.Kartinka

func initRoutes() {
	router.GET("/", showMainPage)
	router.GET("/pictures/view/:id", getPicture).Use(AuthMiddleWare())

	userRoutes := router.Group("/user")
	{
		userRoutes.GET("/register", showRegisterPage)
		userRoutes.POST("/register", RegisterNewUser)
		userRoutes.GET("/login", showLoginPage)
		userRoutes.POST("/login", LoginUser)
	}
	router.GET("/user/logout", LogoutUser).Use(AuthMiddleWare())
}

func main() {
	router = gin.Default()
	router.LoadHTMLGlob("templates/*")

	db, _ := controllers.Setup()
	controller = controllers.NewController(db)

	router.Static("/images", "./images")

	//	gallery = append(gallery, *public.NewKartinka("LV", "nigger"))
	//	gallery = append(gallery, *public.NewKartinka("PP", "hate"))
	//	gallery = append(gallery, *public.NewKartinka("CC", "i"))
	//
	initRoutes()
	router.Run()
}

func render(c *gin.Context, templateName string, data gin.H) {
	switch c.Request.Header.Get("Accept") {
	case "application/json":
		c.JSON(http.StatusOK, data["payload"])
	case "application/xml":
		c.XML(http.StatusOK, data["payload"])

	default:
		c.HTML(http.StatusOK, templateName, data)
	}
}
