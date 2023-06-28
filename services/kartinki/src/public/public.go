package public

import (
	"fmt"
	"image"
	"image/color"
	"image/draw"
	"image/png"
	"log"
	"os"
	"time"
)

type Kartinka struct {
	ID        int    `json: "id"`
	Title     string `json: "title"`
	Comment   string `json: "comment"`
	ImagePath string `json: "image_name"`
}

func NewKartinka(title string, comment string) *Kartinka {
	avatar, err := CreateAvatar(200, title)
	if err != nil {
		return nil
	}

	return &Kartinka{
		123,
		title,
		comment,
		avatar,
	}
}

func CreateAvatar(size int, initials string) (string, error) {
	width, height := size, size
	bgColor, err := hexToRGBA("#764abc")
	if err != nil {
		log.Fatal(err)
	}
	background := image.NewRGBA(image.Rect(0, 0, width, height))
	draw.Draw(background, background.Bounds(), &image.Uniform{C: bgColor},
		image.Point{}, draw.Src)

	filePath := fmt.Sprintf("images/out-%d.png", time.Now().UnixMilli())
	file, err := os.Create(filePath)
	if err != nil {
		return "", err
	}
	png.Encode(file, background)

	return filePath, err
}

func hexToRGBA(hex string) (color.RGBA, error) {
	var (
		rgba             color.RGBA
		err              error
		errInvalidFormat = fmt.Errorf("invalid")
	)
	rgba.A = 0xff
	if hex[0] != '#' {
		return rgba, errInvalidFormat
	}
	hexToByte := func(b byte) byte {
		switch {
		case b >= '0' && b <= '9':
			return b - '0'
		case b >= 'a' && b <= 'f':
			return b - 'a' + 10
		case b >= 'A' && b <= 'F':
			return b - 'A' + 10
		}
		err = errInvalidFormat
		return 0
	}
	switch len(hex) {
	case 7:
		rgba.R = hexToByte(hex[1])<<4 + hexToByte(hex[2])
		rgba.G = hexToByte(hex[3])<<4 + hexToByte(hex[4])
		rgba.B = hexToByte(hex[5])<<4 + hexToByte(hex[6])
	case 4:
		rgba.R = hexToByte(hex[1]) * 17
		rgba.G = hexToByte(hex[2]) * 17
		rgba.B = hexToByte(hex[3]) * 17
	default:
		err = errInvalidFormat
	}
	return rgba, err
}
