FROM golang:1.21.0-alpine3.18
WORKDIR /go/src/app
COPY . .
RUN go mod init api
RUN go build -o api api.go
EXPOSE 8080
CMD ["./api"]