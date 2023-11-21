# Dockerfile for Golang application with curl
FROM golang:1.21.0-alpine3.18

# Instala curl
RUN apk update && apk add curl

WORKDIR /go/src/app
COPY . .
RUN go mod init api
RUN go get github.com/streadway/amqp
RUN go build -o api api.go
EXPOSE 8080
CMD ["./api"]
