package main

import (
	"io"
	"log"
	"net/http"
	"os"
)

// Estructura para las respuestas de autenticación y registro
type Response struct {
	Success bool   `json:"success"`
	Message string `json:"message"`
	// Otros campos según la respuesta esperada
}

func main() {
	r := http.NewServeMux()

	// Manejadores para las rutas de autenticación y registro
	r.HandleFunc("/auth", authHandler)
	r.HandleFunc("/register", registerHandler)

	// Inicia el servidor en el puerto 8080
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

	authEndpoint := usersAPIURL + "/auth"
	authRequest, err := http.NewRequest("POST", authEndpoint, req.Body)
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

	// Resto del código para manejar la respuesta, registrar logs, etc.
	// ...
}

func registerHandler(w http.ResponseWriter, req *http.Request) {
	usersAPIURL := os.Getenv("USERS_API_URL")

	if usersAPIURL == "" {
		log.Println("Variable de entorno USERS_API_URL no definida")
		http.Error(w, "Error interno del servidor", http.StatusInternalServerError)
		return
	}

	registerEndpoint := usersAPIURL + "/users"
	resp, err := http.Post(registerEndpoint, "application/json", req.Body)
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
}
