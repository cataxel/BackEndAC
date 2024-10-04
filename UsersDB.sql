/*
 Database: db_systemac
 */

-- Crear roles
CREATE ROLE administrador;
CREATE ROLE usuario;
CREATE ROLE invitado;

-- Asignar permisos a los roles
-- Permisos para el rol administrador
GRANT ALL PRIVILEGES ON DATABASE db_systemac TO administrador;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO administrador;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO administrador;

-- Permisos para el rol usuario
GRANT CONNECT ON DATABASE db_systemac TO usuario;
GRANT USAGE ON SCHEMA public TO usuario;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO usuario;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO usuario;

-- Permisos para el rol invitado
GRANT CONNECT ON DATABASE db_systemac TO invitado;
GRANT USAGE ON SCHEMA public TO invitado;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO invitado;

-- Crear usuarios
-- Reemplaza 'contraseña' con la contraseña real del usuario
CREATE USER Axel WITH PASSWORD 'Admin2022&';
CREATE USER Ricardo WITH PASSWORD 'Admin2022&';
CREATE USER Beto WITH PASSWORD 'Admin2022&';
CREATE USER Jose WITH PASSWORD 'User2022&';
CREATE USER Abby WITH PASSWORD 'Guest2022&';

-- Asignar roles a los usuarios
-- Reemplaza 'nombre_usuario' con el nombre real del usuario
GRANT administrador TO Axel, Ricardo, Beto;
GRANT usuario TO jose;
GRANT invitado TO Abby;