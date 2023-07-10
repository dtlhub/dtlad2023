package controllers

import (
	"fmt"
	"log"
	"os"

	"gorm.io/driver/mysql"
	"gorm.io/gorm"
)

func newController(db *gorm.DB) *Controller {
	return &Controller{db: db}
}

func SetupControllers(db *gorm.DB) (*LabResultsController, *UserController) {
	return &LabResultsController{db}, &UserController{db}
}

func Setup() (*gorm.DB, error) {

	login := os.Getenv("MYSQL_USER")
	password := os.Getenv("MYSQL_PASSWORD")
	dbname := os.Getenv("MYSQL_DATABASE")

	dsn := fmt.Sprintf("%s:%s@tcp(database:3306)/%s?charset=utf8&parseTime=true", login, password, dbname)

	db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{})
	if err != nil {
		log.Fatal(err.Error())
	}
	if err = db.AutoMigrate(&User{}, &LabResult{}); err != nil {
		log.Fatal(err)
	}
	return db, err
}
