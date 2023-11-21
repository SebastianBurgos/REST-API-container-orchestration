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

// Define structs para las respuestas de autenticación y perfil
type AuthData struct {
	IDUser int    `json:"id_user"`
	Token  string `json:"token"`
}

// Define structs para las respuestas de autenticación y perfil
type UpdateProfileResponse struct {
	Message  string `json:"mensaje"`
	Detalles string `json:"detalles"`
}

type ProfileData struct {
	ID                       int    `json:"id"`
	URLPagina                string `json:"url_pagina"`
	Apodo                    string `json:"apodo"`
	InformacionPublica       int    `json:"informacion_publica"`
	DireccionCorrespondencia string `json:"direccion_correspondencia"`
	Biografia                string `json:"biografia"`
	Organizacion             string `json:"organizacion"`
	Pais                     string `json:"pais"`
}

// Estructura para la respuesta combinada
type CombinedResponse struct {
	AuthData    AuthData    `json:"auth_data"`
	ProfileData ProfileData `json:"profile_data"`
}

// Estructura para la respuesta combinada
type CombinedUpdateResponse struct {
	AuthData              AuthData              `json:"auth_data"`
	UpdateProfileResponse UpdateProfileResponse `json:"updates_profile_response"`
}

// Middleware para habilitar CORS
func enableCors(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")

		if r.Method == "OPTIONS" {
			w.WriteHeader(http.StatusOK)
			return
		}

		next.ServeHTTP(w, r)
	})
}

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

	// Definir manejadores para las rutas de la API
	r.HandleFunc("/auth", authHandler)
	r.HandleFunc("/register", registerHandler)
	r.HandleFunc("/auth-profiles", getProfileHandler)
	r.HandleFunc("/update-profile", updateProfileHandler)
	r.HandleFunc("/health", healthHandler)

	// Aplicar middleware CORS global a todas las rutas
	http.Handle("/", enableCors(r))

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

func getProfileHandler(w http.ResponseWriter, req *http.Request) {
	// Leer el cuerpo JSON de la solicitud (email, clave)
	requestBody, err := io.ReadAll(req.Body)
	if err != nil {
		log.Println("Error al leer el cuerpo de la solicitud:", err)
		http.Error(w, "Error al leer el cuerpo de la solicitud", http.StatusBadRequest)
		return
	}

	// Preparar solicitud de autenticación
	usersAPIURL := os.Getenv("USERS_API_URL")

	if usersAPIURL == "" {
		log.Println("Variable de entorno USERS_API_URL no definida")
		http.Error(w, "Error interno del servidor", http.StatusInternalServerError)
		return
	}

	// Crear la solicitud al servicio de autenticación para obtener el token
	authEndpoint := usersAPIURL + "/auth"
	authRequest, err := http.NewRequest("POST", authEndpoint, bytes.NewReader(requestBody))
	if err != nil {
		log.Println("Error al generar la solicitud al servicio de autenticación:", err)
		http.Error(w, "Error al generar la solicitud al servicio de autenticación", http.StatusInternalServerError)
		return
	}
	authRequest.Header.Set("Content-Type", "application/json") // Establecer el tipo de contenido de la solicitud

	// Realizar la solicitud al servicio de autenticación para obtener el token
	client := &http.Client{}
	authResponse, err := client.Do(authRequest)
	if err != nil {
		log.Println("Error al ejecutar la solicitud al servicio de autenticación:", err)
		http.Error(w, "Error al ejecutar la solicitud al servicio de autenticación", http.StatusInternalServerError)
		return
	}
	defer authResponse.Body.Close()

	// Leer el cuerpo de la respuesta del servicio de autenticación
	authBody, err := io.ReadAll(authResponse.Body)
	if err != nil {
		log.Println("Error al leer la respuesta del servicio de autenticación:", err)
		http.Error(w, "Error al leer la respuesta del servicio de autenticación", http.StatusInternalServerError)
		return
	}

	// Verificar si la autenticación fue exitosa y obtener el token
	var authResponseData map[string]interface{}
	if err := json.Unmarshal(authBody, &authResponseData); err != nil {
		log.Println("Error al decodificar la respuesta JSON del servicio de autenticación:", err)
		http.Error(w, "Error al procesar la respuesta del servicio de autenticación", http.StatusInternalServerError)
		return
	}

	token, ok := authResponseData["token"].(string)
	if !ok {
		log.Println("El token no es una cadena válida")
		http.Error(w, "Error al obtener el token de autenticación", http.StatusInternalServerError)
		return
	}

	var userID int
	idUser, exists := authResponseData["id_user"]
	if exists {
		switch id := idUser.(type) {
		case int:
			userID = id
		case float64:
			userID = int(id)
		default:
			log.Println("El ID de usuario no es un número válido")
			http.Error(w, "Error al obtener el ID de usuario", http.StatusInternalServerError)
			return
		}
	} else {
		log.Println("ID de usuario no encontrado en la respuesta de autenticación")
		http.Error(w, "ID de usuario no encontrado", http.StatusInternalServerError)
		return
	}

	// Preparar solicitud de consulta de perfil
	profilesAPIURL := os.Getenv("PROFILES_API_URL")

	if profilesAPIURL == "" {
		log.Println("Variable de entorno PROFILES_API_URL no definida")
		http.Error(w, "Error interno del servidor", http.StatusInternalServerError)
		return
	}

	// Ahora, con el token obtenido, realizar la solicitud al servicio de perfiles
	profileEndpoint := fmt.Sprintf("%s/profiles/%d", profilesAPIURL, userID)
	profileRequest, err := http.NewRequest("GET", profileEndpoint, nil)
	if err != nil {
		log.Println("Error al generar la solicitud al servicio de perfiles:", err)
		http.Error(w, "Error al generar la solicitud al servicio de perfiles", http.StatusInternalServerError)
		return
	}

	// Establecer el token obtenido en la solicitud de perfil
	profileRequest.Header.Set("Authorization", "Bearer "+token)

	// Realizar la solicitud al servicio de perfiles para obtener el perfil
	profileResponse, err := client.Do(profileRequest)
	if err != nil {
		log.Println("Error al ejecutar la solicitud al servicio de perfiles:", err)
		http.Error(w, "Error al ejecutar la solicitud al servicio de perfiles", http.StatusInternalServerError)
		return
	}
	defer profileResponse.Body.Close()

	// Leer el cuerpo de la respuesta del servicio de perfiles
	profileBody, err := io.ReadAll(profileResponse.Body)
	if err != nil {
		log.Println("Error al leer la respuesta del servicio de perfiles:", err)
		http.Error(w, "Error al leer la respuesta del servicio de perfiles", http.StatusInternalServerError)
		return
	}

	// Establecer el encabezado Content-Type como application/json en la respuesta
	w.Header().Set("Content-Type", "application/json")

	// Crear instancias de AuthData y ProfileData
	var auth AuthData
	var profile ProfileData

	// Decodificar las respuestas del servicio de autenticación y perfiles en sus respectivas estructuras
	if err := json.Unmarshal(authBody, &auth); err != nil {
		log.Println("Error al decodificar la respuesta de autenticación:", err)
		http.Error(w, "Error al decodificar la respuesta de autenticación", http.StatusInternalServerError)
		return
	}

	if err := json.Unmarshal(profileBody, &profile); err != nil {
		log.Println("Error al decodificar la respuesta de perfil:", err)
		http.Error(w, "Error al decodificar la respuesta de perfil", http.StatusInternalServerError)
		return
	}

	// Crear la respuesta combinada
	combinedResponse := CombinedResponse{
		AuthData:    auth,
		ProfileData: profile,
	}

	// Convertir la respuesta combinada a JSON
	responseJSON, err := json.Marshal(combinedResponse)
	if err != nil {
		log.Println("Error al convertir la respuesta a JSON:", err)
		http.Error(w, "Error al convertir la respuesta a JSON", http.StatusInternalServerError)
		return
	}

	// Establecer el encabezado Content-Type como application/json en la respuesta
	w.Header().Set("Content-Type", "application/json")

	// Establecer el código de estado de la respuesta al cliente
	w.WriteHeader(http.StatusOK)

	// Enviar la respuesta combinada al cliente
	_, err = w.Write(responseJSON)
	if err != nil {
		log.Println("Error al enviar la respuesta al cliente:", err)
		http.Error(w, "Error al enviar la respuesta al cliente", http.StatusInternalServerError)
		return
	}
}

func updateProfileHandler(w http.ResponseWriter, req *http.Request) {
	// Decodificar la solicitud JSON
	var requestData map[string]interface{}
	if err := json.NewDecoder(req.Body).Decode(&requestData); err != nil {
		http.Error(w, "Error al decodificar los datos de la solicitud", http.StatusBadRequest)
		return
	}

	// Extraer datos de autenticación
	authData, authExists := requestData["auth_data"].(map[string]interface{})
	if !authExists {
		http.Error(w, "Datos de autenticación no encontrados", http.StatusBadRequest)
		return
	}

	email, emailExists := authData["email"].(string)
	clave, passwordExists := authData["clave"].(string)
	if !emailExists || !passwordExists {
		http.Error(w, "Email o clave no proporcionados", http.StatusBadRequest)
		return
	}

	// Realizar autenticación con los datos proporcionados (aquí va tu lógica de autenticación)
	authPayload := map[string]string{
		"email": email,
		"clave": clave,
	}

	authJSON, err := json.Marshal(authPayload)
	if err != nil {
		log.Println("Error al generar el JSON para autenticación:", err)
		http.Error(w, "Error al generar el JSON para autenticación", http.StatusInternalServerError)
		return
	}

	// Realizar la solicitud al servicio de autenticación
	// Crear la solicitud al servicio de autenticación para obtener el token
	usersAPIURL := os.Getenv("USERS_API_URL")

	if usersAPIURL == "" {
		log.Println("Variable de entorno USERS_API_URL no definida")
		http.Error(w, "Error interno del servidor", http.StatusInternalServerError)
		return
	}

	authEndpoint := usersAPIURL + "/auth"
	authRequest, err := http.NewRequest("POST", authEndpoint, bytes.NewReader(authJSON))
	if err != nil {
		log.Println("Error al generar la solicitud al servicio de autenticación:", err)
		http.Error(w, "Error al generar la solicitud al servicio de autenticación", http.StatusInternalServerError)
		return
	}
	authRequest.Header.Set("Content-Type", "application/json") // Establecer el tipo de contenido de la solicitud

	// Realizar la solicitud al servicio de autenticación para obtener el token
	client := &http.Client{}
	authResponse, err := client.Do(authRequest)
	if err != nil {
		log.Println("Error al ejecutar la solicitud al servicio de autenticación:", err)
		http.Error(w, "Error al ejecutar la solicitud al servicio de autenticación", http.StatusInternalServerError)
		return
	}
	defer authResponse.Body.Close()

	// Leer el cuerpo de la respuesta del servicio de autenticación
	authBody, err := io.ReadAll(authResponse.Body)
	if err != nil {
		log.Println("Error al leer la respuesta del servicio de autenticación:", err)
		http.Error(w, "Error al leer la respuesta del servicio de autenticación", http.StatusInternalServerError)
		return
	}

	// Verificar si la autenticación fue exitosa y obtener el token
	var authResponseData map[string]interface{}
	if err := json.Unmarshal(authBody, &authResponseData); err != nil {
		log.Println("Error al decodificar la respuesta JSON del servicio de autenticación:", err)
		http.Error(w, "Error al procesar la respuesta del servicio de autenticación", http.StatusInternalServerError)
		return
	}

	token, ok := authResponseData["token"].(string)
	if !ok {
		log.Println("El token no es una cadena válida")
		http.Error(w, "Error al obtener el token de autenticación", http.StatusInternalServerError)
		return
	}

	var userID int
	idUser, exists := authResponseData["id_user"]
	if exists {
		switch id := idUser.(type) {
		case int:
			userID = id
		case float64:
			userID = int(id)
		default:
			log.Println("El ID de usuario no es un número válido")
			http.Error(w, "Error al obtener el ID de usuario", http.StatusInternalServerError)
			return
		}
	} else {
		log.Println("ID de usuario no encontrado en la respuesta de autenticación")
		http.Error(w, "ID de usuario no encontrado", http.StatusInternalServerError)
		return
	}

	// Preparar datos para actualizar el perfil
	profileData, profileExists := requestData["profile_data"].(map[string]interface{})
	if !profileExists {
		http.Error(w, "Datos del perfil no encontrados", http.StatusBadRequest)
		return
	}

	// Generar un JSON independiente con los datos del perfil para enviar al servicio de actualización
	profileJSON, err := json.Marshal(profileData)
	if err != nil {
		log.Println("Error al convertir los datos del perfil a JSON:", err)
		http.Error(w, "Error al convertir los datos del perfil a JSON", http.StatusInternalServerError)
		return
	}

	// Preparar solicitud de actualización de perfil
	profilesAPIURL := os.Getenv("PROFILES_API_URL")

	if profilesAPIURL == "" {
		log.Println("Variable de entorno PROFILES_API_URL no definida")
		http.Error(w, "Error interno del servidor", http.StatusInternalServerError)
		return
	}

	updateEndPoint := fmt.Sprintf("%s/profiles/%d", profilesAPIURL, userID)
	updateRequest, err := http.NewRequest("PUT", updateEndPoint, bytes.NewBuffer(profileJSON))
	if err != nil {
		log.Println("Error al crear la solicitud HTTP:", err)
		http.Error(w, "Error al crear la solicitud HTTP", http.StatusInternalServerError)
		return
	}

	// Agregar el token al encabezado de autorización (Bearer Token)
	updateRequest.Header.Set("Authorization", token)

	// Establecer el tipo de contenido del cuerpo de la solicitud
	updateRequest.Header.Set("Content-Type", "application/json")

	// Realizar la solicitud al servicio de actualización de perfil
	updateProfileResponse, err := client.Do(updateRequest)
	if err != nil {
		log.Println("Error al realizar la solicitud:", err)
		http.Error(w, "Error al realizar la solicitud", http.StatusInternalServerError)
		return
	}
	defer updateProfileResponse.Body.Close()

	// Leer el cuerpo de la respuesta del servicio de perfiles
	profileResponseBody, err := io.ReadAll(updateProfileResponse.Body)
	if err != nil {
		log.Println("Error al leer la respuesta del servicio de perfiles:", err)
		http.Error(w, "Error al leer la respuesta del servicio de perfiles", http.StatusInternalServerError)
		return
	}

	// Establecer el encabezado Content-Type y enviar la respuesta al cliente
	w.Header().Set("Content-Type", "application/json")

	// Crear instancias de AuthData y ProfileData
	var authBodyResponse AuthData
	var profileResponse UpdateProfileResponse

	// Decodificar las respuestas del servicio de autenticación y perfiles en sus respectivas estructuras
	if err := json.Unmarshal(authBody, &authBodyResponse); err != nil {
		log.Println("Error al decodificar la respuesta de autenticación:", err)
		http.Error(w, "Error al decodificar la respuesta de autenticación", http.StatusInternalServerError)
		return
	}

	if err := json.Unmarshal(profileResponseBody, &profileResponse); err != nil {
		log.Println("Error al decodificar la respuesta de perfil:", err)
		http.Error(w, "Error al decodificar la respuesta de perfil", http.StatusInternalServerError)
		return
	}

	// Crear la respuesta combinada
	combinedResponse := CombinedUpdateResponse{
		AuthData:              authBodyResponse,
		UpdateProfileResponse: profileResponse,
	}

	// Convertir la respuesta combinada a JSON
	responseJSON, err := json.Marshal(combinedResponse)
	if err != nil {
		log.Println("Error al convertir la respuesta a JSON:", err)
		http.Error(w, "Error al convertir la respuesta a JSON", http.StatusInternalServerError)
		return
	}

	// Establecer el encabezado Content-Type como application/json en la respuesta
	w.Header().Set("Content-Type", "application/json")

	// Establecer el código de estado de la respuesta al cliente
	w.WriteHeader(http.StatusOK)

	// Enviar la respuesta combinada al cliente
	_, err = w.Write(responseJSON)
	if err != nil {
		log.Println("Error al enviar la respuesta al cliente:", err)
		http.Error(w, "Error al enviar la respuesta al cliente", http.StatusInternalServerError)
		return
	}
}

func healthHandler(w http.ResponseWriter, req *http.Request) {
	fmt.Fprintf(w, "OK")
}
