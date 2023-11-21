# Docker Compose Orchestration System Description

This Docker Compose orchestration system is designed to streamline the deployment of a robust microservices architecture. It seamlessly integrates various services, fostering efficient communication and data management within the ecosystem.

## Services

### User Authentication API

- **Description:** A secure API responsible for user authentication. It provides authentication services for users interacting with the system.
- **Connection:** Establishes connections with the MySQL database to authenticate users.

### Logging API

- **Description:** A dynamic API tailored for logging events and activities within the system. It plays a pivotal role in tracking and monitoring user actions.
- **Connection:** Interacts with RabbitMQ for efficient message queuing and distribution of log-related data.

### Profiles Service

- **Description:** Manages user profiles within the system, automatically creating a profile for newly registered users in the User Service. It stores user-specific information and allows for convenient updates to profile data.
- **Connections:** Tightly integrated with the User Service, triggering profile creation upon user registration and providing interfaces for users to update their profile information seamlessly.

### Gateway Service

- **Description:** Acts as an intermediary for incoming user requests, directing them to various services within the system. It serves as a central point for handling and managing user interactions, orchestrating communication between the user and multiple backend services.
- **Connections:** Receives user requests and intelligently routes them to appropriate services based on the request type or endpoint. It aggregates and relays the responses from different services back to the user, providing a unified interface for user interaction with the system.

### MySQL Service

- **Description:** A robust and scalable MySQL database service for persistent data storage. It serves as the backbone for storing user-related information and system data.
- **Connections:** Both the User Authentication API and Logging API connect to this service for data storage and retrieval.

### RabbitMQ Service

- **Description:** A powerful message broker service that facilitates efficient communication between microservices. It handles the queuing and distribution of log-related messages.
- **Connections:** The Logging API utilizes RabbitMQ for seamless delivery of log messages to downstream systems.


## Running the System

To deploy this system, make sure you are in the root directory containing the `docker-compose.yml` file. Then, execute the following command:

```bash
docker compose up
```

## Running Tests

To test this system (at Linux or Windows with Git Bash Terminal), make sure you are in the test directory containing the `script.sh` file. Then, execute the following command:

```bash
./script.sh
```
