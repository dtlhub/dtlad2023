package main

import (
	"errors"
	"fmt"
	"net/http"
	"strconv"

	"github.com/YellowPhil/pwnAD/public"
	"github.com/YellowPhil/pwnAD/user"
	"github.com/gin-gonic/gin"
)

func showMainPage(g *gin.Context) {
	render(g, "index.html", gin.H{"header": "Home page", "payload": gallery})
}

func getPicById(id int) (*public.Kartinka, error) {
	for _, k := range gallery {
		if k.ID == id {
			return &k, nil
		}
	}
	return nil, errors.New("Picture with id " + string(id) + " not found")
}

func getPicture(c *gin.Context) {

	var (
		id       int
		err      error
		kartinka *public.Kartinka
	)
	if id, err = strconv.Atoi(c.Param("id")); err != nil {
		c.AbortWithError(http.StatusNotFound, errors.New("Bad id"))
	}

	if kartinka, err = getPicById(id); err == nil {
		render(c, "picture.html", gin.H{
			"title":   kartinka.Title,
			"picture": kartinka,
		})

	} else {
		c.AbortWithError(http.StatusNotFound, errors.New(fmt.Sprintf("Could not locate picture with id %d", id)))
	}
}

func showRegisterPage(c *gin.Context) {
	render(c, "register.html", gin.H{"title": "Register"})
}

func RegisterNewUser(c *gin.Context) {
	username := c.PostForm("username")
	password := c.PostForm("password")

	if _, err := user.Register(username, password); err != nil {
		c.AbortWithError(http.StatusBadRequest, err)
	}
	authenticateUser(c)

	render(c, "registration-successful.html", gin.H{"title": "Registered successfully"})
}

func showLoginPage(c *gin.Context) {
	render(c, "login.html", gin.H{"title": "Login"})
}

func LoginUser(c *gin.Context) {
	username := c.PostForm("username")
	password := c.PostForm("password")

	if !user.IsUserValid(username, password) {
		c.AbortWithError(http.StatusBadRequest, fmt.Errorf("Invalid username or password"))
	}
	authenticateUser(c)

	render(c, "login-successful.html", gin.H{"title": "Login successful"})
}

func LogoutUser(c *gin.Context) {
	deauthenticateUser(c)
	c.Redirect(http.StatusTemporaryRedirect, "/")
}
