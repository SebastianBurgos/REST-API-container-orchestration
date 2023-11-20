package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net"
	"net/http"
	"os"
	"time"

	"github.com/streadway/amqp"
)

var ch *amqp.Channel
var queueName string

type Response struct {
	Success bool   `json:"success"`
	Message string `json:"message"`
}

func connectToRabbitMQ() (*amqp.Connection, error) {
	rabbitMQService := os.Getenv("RABBITMQ_SERVICE")
	rabbitMQURL := fmt.Sprintf("amqp://guest:guest@%s:5672/", rabbitMQService)

	for {
		conn, err := amqp.Dial(rabbitMQURL)
		if err == nil {
			return conn, nil
		}

		log.Printf("Error al conectar con RabbitMQ: %s. Reintentando en 5 segundos...", err)
		time.Sleep(5 * time.Second)
	}
}

func main() {
	conn, err := connectToRabbitMQ()
	if err != nil {
		log.Fatalf("No se pudo conectar con RabbitMQ: %s", err)
	}
	defer conn.Close()

	ch, err = conn.Channel()
	if err != nil {
		log.Fatalf("Error al abrir un canal: %s", err)
	}
	defer ch.Close()

	queueName = "logs"
	_, err = ch.QueueDeclare(
		queueName,
		true,
		false,
		false,
		false,
		nil,
	)
	if err != nil {
		log.Fatalf("Error al declarar la cola: %s", err)
	}

	r := http.NewServeMux()
	r.HandleFunc("/auth", authHandler)
	r.HandleFunc("/register", registerHandler)

	log.Println("Servidor Gateway Iniciado en el puerto 8080")
	log.Fatal(http.ListenAndServe(":8080", r))
}

func authHandler(w http.ResponseWriter, req *http.Request) {
	usersAPIURL := os.Getenv("USERS_API_URL")

	if usersAPIURL == "" {
		log.Println("Variable de entorno USERS_API_URL no definida")
		http.Error(w, "Error interno del servidor", http.StatusInternalServerError)
		return
	}

	// Leer el cuerpo JSON de la solicitud
	reqBody, err := io.ReadAll(req.Body)
	if err != nil {
		log.Println("Error al leer el cuerpo de la solicitud:", err)
		http.Error(w, "Error interno del servidor", http.StatusInternalServerError)
		return
	}
	defer req.Body.Close()

	var autenticacion map[string]string
	if err := json.Unmarshal(reqBody, &autenticacion); err != nil {
		log.Println("Error al decodificar el cuerpo JSON:", err)
		http.Error(w, "Error en el formato de la solicitud", http.StatusBadRequest)
		return
	}

	authEndpoint := usersAPIURL + "/auth"
	authRequest, err := http.NewRequest("POST", authEndpoint, bytes.NewReader(reqBody))
	if err != nil {
		log.Println("Error al generar la solicitud al servicio de autenticacion:", err)
		http.Error(w, "Error al generar la solicitud al servicio de autenticacion", http.StatusInternalServerError)
		return
	}

	authRequest.Header.Set("Content-Type", "application/json") // Establecer el tipo de contenido de la solicitud

	// Ejecutar la solicitud al servicio users_api para autenticación
	client := &http.Client{}
	authResponse, err := client.Do(authRequest)
	if err != nil {
		log.Println("Error al ejecutar la solicitud al servicio de autenticacion:", err)
		http.Error(w, "Error al ejecutar la solicitud al servicio de autenticacion", http.StatusInternalServerError)
		return
	}
	defer authResponse.Body.Close()

	// Leer el cuerpo de la respuesta del servicio users_api
	responseBody, err := io.ReadAll(authResponse.Body)
	if err != nil {
		log.Println("Error al leer la respuesta del servicio de autenticacion:", err)
		http.Error(w, "Error al leer la respuesta del servicio de autenticacion", http.StatusInternalServerError)
		return
	}

	var authResponseData map[string]interface{}
	if err := json.Unmarshal(responseBody, &authResponseData); err != nil {
		log.Println("Error al decodificar la respuesta JSON:", err)
		http.Error(w, "Error al procesar la respuesta del servicio de autenticacion", http.StatusInternalServerError)
		return
	}

	token, ok := authResponseData["token"].(string)
	if !ok {
		log.Println("El token no es una cadena válida")
		http.Error(w, "Error al obtener el token", http.StatusInternalServerError)
		return
	}

	// Establecer el encabezado Content-Type como application/json en la respuesta
	w.Header().Set("Content-Type", "application/json")

	// Establecer el código de estado HTTP de la respuesta del servicio users_api en la respuesta al cliente
	w.WriteHeader(authResponse.StatusCode)

	// Copiar el cuerpo de la respuesta del servicio users_api al cuerpo de la respuesta al cliente
	_, err = w.Write(responseBody)
	if err != nil {
		log.Println("Error al enviar la respuesta al cliente:", err)
		http.Error(w, "Error al enviar la respuesta al cliente", http.StatusInternalServerError)
		return
	}

	// Generar mensaje para logs
	tipoLog := "GATEWAY"
	metodo := "POST"
	ruta := "/auth"
	modulo := "API.PY"
	application := "GATEWAY_API_REST"
	ip, _, _ := net.SplitHostPort(req.RemoteAddr)
	usuarioAutenticado := fmt.Sprintf("USUARIO AUTENTICADO: %s", autenticacion["email"])

	mensaje := "UN USUARIO SE HA AUTENTICADO POR MEDIO DE LA API GATEWAY."

	bodymessage := fmt.Sprintf("%s#%s#%s#%s#%s#%s#%s#%s#%s#%s",
		tipoLog, metodo, ruta, modulo, application, time.Now().Format("2006-01-02 15:04:05"), ip, usuarioAutenticado, token, mensaje)

	// Publicar el mensaje en la cola 'logs'
	err = ch.Publish(
		"",        // exchange
		queueName, // routing key
		false,     // mandatory
		false,     // immediate
		amqp.Publishing{
			ContentType: "text/plain",
			Body:        []byte(bodymessage),
		},
	)
	if err != nil {
		log.Fatalf("Error al publicar mensaje: %s", err)
	}

	fmt.Println("Mensaje desde servicio gateway enviado a la cola de logs")
}

func registerHandler(w http.ResponseWriter, req *http.Request) {
	usersAPIURL := os.Getenv("USERS_API_URL")

	if usersAPIURL == "" {
		log.Println("Variable de entorno USERS_API_URL no definida")
		http.Error(w, "Error interno del servidor", http.StatusInternalServerError)
		return
	}

	// Leer el cuerpo de la solicitud y almacenarlo en una variable
	requestBody, err := io.ReadAll(req.Body)
	if err != nil {
		log.Println("Error al leer el cuerpo de la solicitud:", err)
		http.Error(w, "Error interno del servidor", http.StatusInternalServerError)
		return
	}

	// Cerrar el cuerpo de la solicitud para liberar recursos
	defer req.Body.Close()

	registerEndpoint := usersAPIURL + "/users"
	resp, err := http.Post(registerEndpoint, "application/json", bytes.NewBuffer(requestBody))
	if err != nil {
		log.Println("Error al realizar la solicitud al servicio de registro:", err)
		http.Error(w, "Error al realizar la solicitud al servicio de registro", http.StatusInternalServerError)
		return
	}
	defer resp.Body.Close()

	// Leer la respuesta del servicio de registro
	responseBody, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Println("Error al leer la respuesta del servicio de registro:", err)
		http.Error(w, "Error al leer la respuesta del servicio de registro", http.StatusInternalServerError)
		return
	}

	// Establecer el encabezado Content-Type como application/json en la respuesta
	w.Header().Set("Content-Type", "application/json")

	// Establecer el código de estado de la respuesta al cliente
	w.WriteHeader(resp.StatusCode)

	// Copiar el cuerpo de la respuesta del servicio de registro como respuesta al cliente
	_, err = w.Write(responseBody)
	if err != nil {
		log.Println("Error al enviar la respuesta al cliente:", err)
		http.Error(w, "Error al enviar la respuesta al cliente", http.StatusInternalServerError)
		return
	}

	// Decodificar el cuerpo de la solicitud que se leyó previamente
	var user map[string]string
	if err := json.Unmarshal(requestBody, &user); err != nil {
		log.Println("Error al decodificar el cuerpo JSON:", err)
		http.Error(w, "Error en el formato de la solicitud", http.StatusBadRequest)
		return
	}

	// Generar mensaje para logs
	tipoLog := "GATEWAY"
	metodo := "POST"
	ruta := "/register"
	modulo := "API.PY"
	application := "GATEWAY_API_REST"
	ip, _, _ := net.SplitHostPort(req.RemoteAddr)
	usuarioAutenticado := fmt.Sprintf("USUARIO REGISTRADO: %s %s", user["nombre"], user["apellido"])

	mensaje := "UN USUARIO SE HA REGISTRADO POR MEDIO DE LA API GATEWAY."

	bodymessage := fmt.Sprintf("%s#%s#%s#%s#%s#%s#%s#%s#%s#%s",
		tipoLog, metodo, ruta, modulo, application, time.Now().Format("2006-01-02 15:04:05"), ip, usuarioAutenticado, "NO TOKEN", mensaje)

	// Publicar el mensaje en la cola 'logs'
	err = ch.Publish(
		"",        // exchange
		queueName, // routing key
		false,     // mandatory
		false,     // immediate
		amqp.Publishing{
			ContentType: "text/plain",
			Body:        []byte(bodymessage),
		},
	)
	if err != nil {
		log.Fatalf("Error al publicar mensaje: %s", err)
	}

	fmt.Println("Mensaje desde servicio gateway enviado a la cola de logs")
}
