-- Conexión a la base de datos
CREATE DATABASE IF NOT EXISTS profiles_db;
USE profiles_db;

-- Creación de la tabla Usuario
CREATE TABLE IF NOT EXISTS Perfil (
    id INT PRIMARY KEY,
    url_pagina VARCHAR(255) NOT NULL,
    apodo VARCHAR(60) NOT NULL,
    informacion_publica BOOLEAN NOT NULL,
    direccion_correspondencia VARCHAR(255) NOT NULL,
    biografia VARCHAR(255) NOT NULL,
    organizacion VARCHAR(255) NOT NULL,
    pais VARCHAR(255) NOT NULL
);

-- Creación de la tabla RedesSociales
CREATE TABLE IF NOT EXISTS RedesSociales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    url_rs VARCHAR(255) NOT NULL,
    perfil_id INT NOT NULL,
    FOREIGN KEY (perfil_id) REFERENCES Perfil(id)
);

-- Inserción de datos de prueba en la tabla Usuario
INSERT INTO Perfil (id, url_pagina, apodo, informacion_publica, direccion_correspondencia, biografia, organizacion, pais)
VALUES
    (1, 'juanperez.com', 'JuaniPerro', false, 'cl 19 #3 2-100', 'Juanito nacio en macondo y estudio leyes', 'FARC', 'Colombia'),
    (2, 'mariazungona.com', 'Marilu123', true, 'Av. Principal #45', 'Marilu es una apasionada de la música y le encanta viajar.', 'MusicCorp', 'Argentina'),
    (3, 'carlosote.com', 'CG1995', true, 'Calle Mayor #7', 'Carlos es un apasionado por la tecnología y siempre está buscando aprender algo nuevo.', 'Tech Innovators', 'España'),
    (4, 'analuferita.com', 'AnaMtz92', true, 'Carrera 12 #34-56', 'Ana es una amante de los animales y dedica su tiempo libre a cuidar a perros y gatos abandonados.', 'Animal Lovers Foundation', 'México'),
    (5, 'luisandro', 'LuiRod98', true, 'Rua Principal #23', 'Luis es un fanático del deporte y disfruta jugando al fútbol en su tiempo libre.', 'Sports Unlimited', 'Brasil');

-- Inserción de datos de prueba en la tabla RedesSociales
INSERT INTO RedesSociales (nombre, url_rs, perfil_id)
VALUES
    ('Facebook', 'https://www.facebook.com/juanperez', 1),
    ('Twitter', 'https://twitter.com/juanperez', 1),
    ('Instagram', 'https://www.instagram.com/juanperez', 1),
    ('Facebook', 'https://www.facebook.com/mariaz', 2),
    ('Twitter', 'https://twitter.com/mariaz', 2),
    ('Instagram', 'https://www.instagram.com/mariaz', 2),
    ('Facebook', 'https://www.facebook.com/carlosote', 3),
    ('Twitter', 'https://twitter.com/carlosote', 3),
    ('Instagram', 'https://www.instagram.com/carlosote', 3),
    ('Facebook', 'https://www.facebook.com/analuferita', 4),
    ('Twitter', 'https://twitter.com/analuferita', 4),
    ('Instagram', 'https://www.instagram.com/analuferita', 4),
    ('Facebook', 'https://www.facebook.com/luisandro', 5),
    ('Twitter', 'https://twitter.com/luisandro', 5),
    ('Instagram', 'https://www.instagram.com/luisandro', 5);
