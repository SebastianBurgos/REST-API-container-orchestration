-- Conexión a la base de datos
CREATE DATABASE IF NOT EXISTS ApiDB;
USE ApiDB;

-- Creación de la tabla Usuario
CREATE TABLE IF NOT EXISTS Usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    clave VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inserción de datos de prueba en la tabla Usuario
INSERT INTO Usuario (nombre, apellido, email, clave, fecha_nacimiento)
VALUES
    ('Juan', 'Pérez', 'juan@example.com', 'juan', '1990-05-15'),
    ('María', 'López', 'maria@example.com', 'maria', '1988-12-03'),
    ('Carlos', 'García', 'carlos@example.com', 'carlos', '1995-09-22'),
    ('Ana', 'Martínez', 'ana@example.com', 'ana', '1992-07-11'),
    ('Luis', 'Rodríguez', 'luis@example.com', 'luis', '1998-04-28');
    