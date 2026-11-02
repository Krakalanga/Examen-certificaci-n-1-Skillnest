CREATE DATABASE viajes_usuario
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE viajes_usuario;


CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE viajes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    destino VARCHAR(100) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    itinerario VARCHAR(40) NOT NULL,

    organizador_id INT NOT NULL,

    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (organizador_id)
    REFERENCES usuarios(id)
    ON DELETE CASCADE
);


CREATE TABLE viajeros (
    id INT AUTO_INCREMENT PRIMARY KEY,

    usuario_id INT NOT NULL,
    viaje_id INT NOT NULL,

    fecha_union TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (usuario_id)
    REFERENCES usuarios(id)
    ON DELETE CASCADE,

    FOREIGN KEY (viaje_id)
    REFERENCES viajes(id)
    ON DELETE CASCADE,

    UNIQUE (usuario_id, viaje_id)
);