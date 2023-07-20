FROM golang:alpine3.18 AS builder

RUN apk update

WORKDIR /go/build/webServer

COPY . .

RUN go get -d -v
RUN ls /go/build/webServer/templates
RUN GOOS=linux GOARCH=amd64 go build -o /go/build/webServer/server -ldflags="-w -s"

FROM scratch

COPY --from=builder /go/build/webServer/server server
COPY --from=builder /go/build/webServer/templates/ templates

ENTRYPOINT ["/server"]
