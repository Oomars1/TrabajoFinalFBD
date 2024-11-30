-- Eliminar tablas si existen
DROP TABLE IF EXISTS bitacora, log, proyecto, gasolineras, usuarios, vehiculos, rol;

-- Crear tabla rol
CREATE TABLE rol (
    id_rol INT AUTO_INCREMENT PRIMARY KEY,
    descripcion TEXT NOT NULL
);

-- Crear tabla usuarios
CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    password VARCHAR(55) NOT NULL,
    id_rol INT,
    activo BOOLEAN DEFAULT FALSE,
    username VARCHAR(30) UNIQUE,
    FOREIGN KEY (id_rol) REFERENCES rol(id_rol)
);

-- Crear tabla vehiculos
CREATE TABLE vehiculos (
    id_vehiculo INT AUTO_INCREMENT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modelo VARCHAR(50) NOT NULL,
    marca VARCHAR(50) NOT NULL,
    placa VARCHAR(30) UNIQUE NOT NULL,
    rendimiento VARCHAR(30),
    galonaje FLOAT,
    tipo_combustible VARCHAR(25) NOT NULL
);

-- Crear tabla gasolineras
CREATE TABLE gasolineras (
    id_gasolinera INT AUTO_INCREMENT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    nombre VARCHAR(50) NOT NULL,
    direccion VARCHAR(60) NOT NULL
);

-- Crear tabla proyecto
CREATE TABLE proyecto (
    id_proyecto INT AUTO_INCREMENT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    nombre VARCHAR(50) NOT NULL,
    direccion VARCHAR(60) NOT NULL,
    activo BOOLEAN DEFAULT FALSE
);

-- Crear tabla log
CREATE TABLE log (
    id_log INT AUTO_INCREMENT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    descripcion TEXT NOT NULL,
    id_usuario INT,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

-- Crear tabla bitacora
CREATE TABLE bitacora (
    id_bitacora INT AUTO_INCREMENT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    comentario TEXT,
    km_inicial INT NOT NULL,
    km_final INT NOT NULL,
    num_galones FLOAT NOT NULL,
    costo FLOAT NOT NULL,
    tipo_gasolina VARCHAR(30) NOT NULL,
    id_usuario INT,
    id_vehiculo INT,
    id_gasolinera INT,
    id_proyecto INT,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_vehiculo) REFERENCES vehiculos(id_vehiculo),
    FOREIGN KEY (id_gasolinera) REFERENCES gasolineras(id_gasolinera),
    FOREIGN KEY (id_proyecto) REFERENCES proyecto(id_proyecto)
);

-- Crear el trigger para log de usuario
DELIMITER //

CREATE TRIGGER log_usuario_login
AFTER UPDATE ON usuarios
FOR EACH ROW
BEGIN
    IF NEW.activo = TRUE AND OLD.activo = FALSE THEN
        INSERT INTO log (created_at, descripcion, id_usuario)
        VALUES (
            CURRENT_TIMESTAMP,
            CONCAT('Usuario: ', NEW.username, ', Nombre: ', NEW.nombre, ' ', NEW.apellido, 
                   ', Rol: ', NEW.id_rol, ', Inició sesión.'),
            NEW.id_usuario
        );
    END IF;
END //

DELIMITER ;
