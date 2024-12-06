/*
 Database: db_systemac
 */
-- Crear la base de datos con codificación UTF-8
CREATE DATABASE db_systemac
    WITH
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TEMPLATE = template0;

-- Usar la base de datos creada
\c db_systemac;


-- Crear tabla de Roles
DROP TABLE IF EXISTS Roles CASCADE;
CREATE TABLE Roles (
    id SERIAL PRIMARY KEY, -- Identificador único de la tabla Roles
    guid UUID UNIQUE NOT NULL, -- GUID único para la tabla Roles
    nombre VARCHAR(50) NOT NULL, -- Nombre del rol
    descripcion TEXT -- Descripción del rol
);
CREATE INDEX idx_roles_nombre ON Roles(nombre);

-- Crear tabla de Usuarios
DROP TABLE IF EXISTS Usuarios CASCADE;
CREATE TABLE Usuarios (
    id SERIAL PRIMARY KEY, -- Identificador único de la tabla Usuarios
    guid UUID UNIQUE NOT NULL, -- GUID único para la tabla Usuarios
    nombre VARCHAR(100) NOT NULL, -- Nombre del usuario
    correo VARCHAR(100) UNIQUE NOT NULL, -- Correo electrónico único del usuario
    contraseña VARCHAR(255) NOT NULL, -- Contraseña del usuario
    rol_id INTEGER REFERENCES Roles(id) ON DELETE SET NULL -- Referencia al rol del usuario
);
CREATE INDEX idx_usuarios_correo ON Usuarios(correo);
CREATE INDEX idx_usuarios_rol_id ON Usuarios(rol_id);

-- Crear tabla de Perfiles
DROP TABLE IF EXISTS Perfiles CASCADE;
CREATE TABLE Perfiles (
    id SERIAL PRIMARY KEY, -- Identificador único de la tabla Perfiles
    guid UUID UNIQUE NOT NULL, -- GUID único para la tabla Perfiles
    usuario_id INTEGER REFERENCES Usuarios(id) ON DELETE CASCADE, -- Referencia al usuario
    telefono VARCHAR(15), -- Teléfono del usuario
    direccion TEXT, -- Dirección del usuario
    carrera TEXT, -- Carrera del perfil si aplica
    numero_control int, -- numero control del perfil
    imagen TEXT -- nombre de imagen
);
CREATE INDEX idx_perfiles_usuario_id ON Perfiles(usuario_id);
CREATE INDEX inx_perfiles_numero_control ON Perfiles(numero_control);

-- Crear tabla de Sesiones
DROP TABLE IF EXISTS Sesiones CASCADE;
CREATE TABLE Sesiones (
    id SERIAL PRIMARY KEY, -- Identificador único de la tabla Sesiones
    guid UUID UNIQUE NOT NULL, -- GUID único para la tabla Sesiones
    usuario_id INTEGER REFERENCES Usuarios(id) ON DELETE CASCADE, -- Referencia al usuario
    fecha_inicio TIMESTAMP NOT NULL, -- Fecha y hora de inicio de la sesión
    fecha_fin TIMESTAMP -- Fecha y hora de fin de la sesión
);
CREATE INDEX idx_sesiones_usuario_id ON Sesiones(usuario_id);
CREATE INDEX idx_sesiones_fecha_inicio ON Sesiones(fecha_inicio);

-- Crear tabla de Actividades
DROP TABLE IF EXISTS Actividades CASCADE;
CREATE TABLE Actividades (
    id SERIAL PRIMARY KEY, -- Identificador único de la tabla Actividades
    guid UUID UNIQUE NOT NULL, -- GUID único para la tabla Actividades
    nombre VARCHAR(100) NOT NULL, -- Nombre de la actividad
    descripcion TEXT -- Descripción de la actividad
);
CREATE INDEX idx_actividades_nombre ON Actividades(nombre);

-- Crear tabla de Asistencia
DROP TABLE IF EXISTS Asistencia CASCADE;
CREATE TABLE Asistencia (
    id SERIAL PRIMARY KEY, -- Identificador único de la tabla Asistencia
    guid UUID UNIQUE NOT NULL, -- GUID único para la tabla Asistencia
    usuario_id INTEGER REFERENCES Usuarios(id) ON DELETE CASCADE, -- Referencia al usuario
    actividad_id INTEGER REFERENCES Actividades(id) ON DELETE CASCADE, -- Referencia a la actividad
    fecha_registro TIMESTAMP NOT NULL, -- Fecha y hora de registro de la asistencia
    estado VARCHAR(10) CHECK (estado IN ('presente', 'ausente')) -- Estado de la asistencia (presente o ausente)
);
CREATE INDEX idx_asistencia_usuario_id ON Asistencia(usuario_id);
CREATE INDEX idx_asistencia_actividad_id ON Asistencia(actividad_id);
CREATE INDEX idx_asistencia_fecha_registro ON Asistencia(fecha_registro);


-- Crear tabla de Grupos
DROP TABLE IF EXISTS Grupos CASCADE;
CREATE TABLE Grupos (
    id SERIAL PRIMARY KEY, -- Identificador único de la tabla Grupos
    guid UUID UNIQUE NOT NULL, -- GUID único para la tabla Grupos
    descripcion TEXT NOT NULL, -- Descripción del grupo
    ubicacion TEXT NOT NULL, -- Descripción del grupo
    hora_inicial TIME NOT NULL, -- Hora inicial del grupo
    hora_final TIME NOT NULL, -- Hora final del grupo
    fecha_inicial DATE NOT NULL, -- Fecha inicial del grupo
    fecha_final DATE NOT NULL, -- Fecha final del grupo
    capacidad INTEGER NOT NULL, -- Capacidad de la actividad

    usuario_id INTEGER REFERENCES Usuarios(id) ON DELETE CASCADE, -- Referencia al usuario
    actividad_id INTEGER REFERENCES Actividades(id) ON DELETE CASCADE -- Referencia a la actividad
);

-- Índices para mejorar el rendimiento
CREATE INDEX idx_grupos_usuario_id ON Grupos(usuario_id);
CREATE INDEX idx_grupos_actividad_id ON Grupos(actividad_id);
CREATE INDEX idx_grupos_fecha_inicial ON Grupos(fecha_inicial);
CREATE INDEX idx_grupos_hora_inicial ON Grupos(hora_inicial);


-- Crear tabla de Inscripciones
DROP TABLE IF EXISTS Inscripciones CASCADE;
CREATE TABLE Inscripciones (
    id SERIAL PRIMARY KEY, -- Identificador único de la tabla Inscripciones
    guid UUID UNIQUE NOT NULL, -- GUID único para la tabla Inscripciones
    usuario_id INTEGER REFERENCES Usuarios(id) ON DELETE CASCADE, -- Referencia al usuario
    grupo_id INTEGER REFERENCES Grupos(id) ON DELETE CASCADE, -- Referencia a la actividad
    fecha_inscripcion TIMESTAMP NOT NULL, -- Fecha y hora de inscripción
    estado VARCHAR(10) CHECK (estado IN ('inscrito', 'en espera')) -- Estado de la inscripción (inscrito o en espera)
);
CREATE INDEX idx_inscripciones_usuario_id ON Inscripciones(usuario_id);
CREATE INDEX idx_inscripciones_grupo_id ON Inscripciones(grupo_id);
CREATE INDEX idx_inscripciones_fecha_inscripcion ON Inscripciones(fecha_inscripcion);

-- Crear tabla de Listas de Espera
DROP TABLE IF EXISTS Listas_Espera CASCADE;
CREATE TABLE Listas_Espera (
    id SERIAL PRIMARY KEY, -- Identificador único de la tabla Listas de Espera
    guid UUID UNIQUE NOT NULL, -- GUID único para la tabla Listas de Espera
    usuario_id INTEGER REFERENCES Usuarios(id) ON DELETE CASCADE, -- Referencia al usuario
    actividad_id INTEGER REFERENCES Actividades(id) ON DELETE CASCADE, -- Referencia a la actividad
    fecha_registro TIMESTAMP NOT NULL -- Fecha y hora de registro en la lista de espera
);
CREATE INDEX idx_listas_espera_usuario_id ON Listas_Espera(usuario_id);
CREATE INDEX idx_listas_espera_actividad_id ON Listas_Espera(actividad_id);
CREATE INDEX idx_listas_espera_fecha_registro ON Listas_Espera(fecha_registro);

-- Crear tabla de Evaluaciones
DROP TABLE IF EXISTS Evaluaciones CASCADE;
CREATE TABLE Evaluaciones (
    id SERIAL PRIMARY KEY, -- Identificador único de la tabla Evaluaciones
    guid UUID UNIQUE NOT NULL, -- GUID único para la tabla Evaluaciones
    usuario_id INTEGER REFERENCES Usuarios(id) ON DELETE CASCADE, -- Referencia al usuario
    actividad_id INTEGER REFERENCES Actividades(id) ON DELETE CASCADE, -- Referencia a la actividad
    calificacion DECIMAL(2, 1) CHECK (calificacion >= 0 AND calificacion <= 5), -- Calificación de la actividad
    comentarios TEXT -- Comentarios sobre la actividad
);
CREATE INDEX idx_evaluaciones_usuario_id ON Evaluaciones(usuario_id);
CREATE INDEX idx_evaluaciones_actividad_id ON Evaluaciones(actividad_id);
CREATE INDEX idx_evaluaciones_calificacion ON Evaluaciones(calificacion);

-- Crear tabla de Participaciones
DROP TABLE IF EXISTS Participaciones CASCADE;
CREATE TABLE Participaciones (
    id SERIAL PRIMARY KEY, -- Identificador único de la tabla Participaciones
    guid UUID UNIQUE NOT NULL, -- GUID único para la tabla Participaciones
    usuario_id INTEGER REFERENCES Usuarios(id) ON DELETE CASCADE, -- Referencia al usuario
    actividad_id INTEGER REFERENCES Actividades(id) ON DELETE CASCADE, -- Referencia a la actividad
    fecha_participacion TIMESTAMP NOT NULL -- Fecha y hora de participación
);
CREATE INDEX idx_participaciones_usuario_id ON Participaciones(usuario_id);
CREATE INDEX idx_participaciones_actividad_id ON Participaciones(actividad_id);
CREATE INDEX idx_participaciones_fecha_participacion ON Participaciones(fecha_participacion);

-- Crear tabla de Notificaciones
DROP TABLE IF EXISTS Notificaciones CASCADE;
CREATE TABLE Notificaciones (
    id SERIAL PRIMARY KEY, -- Identificador único de la tabla Notificaciones
    guid UUID UNIQUE NOT NULL, -- GUID único para la tabla Notificaciones
    usuario_id INTEGER REFERENCES Usuarios(id) ON DELETE CASCADE, -- Referencia al usuario
    asunto VARCHAR(255) NOT NULL, -- Asunto de la notificación
    mensaje TEXT NOT NULL, -- Mensaje de la notificación
    fecha_envio TIMESTAMP NOT NULL -- Fecha y hora de envío de la notificación
);
CREATE INDEX idx_notificaciones_usuario_id ON Notificaciones(usuario_id);
CREATE INDEX idx_notificaciones_fecha_envio ON Notificaciones(fecha_envio);

-- Crear tabla de Anuncios
DROP TABLE IF EXISTS Anuncios CASCADE;
CREATE TABLE Anuncios (
    id SERIAL PRIMARY KEY, -- Identificador único de la tabla Anuncios
    guid UUID UNIQUE NOT NULL, -- GUID único para la tabla Anuncios
    administrador_id INTEGER REFERENCES Usuarios(id) ON DELETE CASCADE, -- Referencia al administrador
    titulo VARCHAR(255) NOT NULL, -- Título del anuncio
    contenido TEXT NOT NULL, -- Contenido del anuncio
    fecha_publicacion TIMESTAMP NOT NULL -- Fecha y hora de publicación del anuncio
);
CREATE INDEX idx_anuncios_administrador_id ON Anuncios(administrador_id);
CREATE INDEX idx_anuncios_fecha_publicacion ON Anuncios(fecha_publicacion);

-- Crear tabla de Sincronizaciones
DROP TABLE IF EXISTS Sincronizaciones CASCADE;
CREATE TABLE Sincronizaciones (
    id SERIAL PRIMARY KEY, -- Identificador único de la tabla Sincronizaciones
    guid UUID UNIQUE NOT NULL, -- GUID único para la tabla Sincronizaciones
    fecha TIMESTAMP NOT NULL, -- Fecha y hora de la sincronización
    estado VARCHAR(50) NOT NULL, -- Estado de la sincronización
    detalles TEXT -- Detalles de la sincronización
);
CREATE INDEX idx_sincronizaciones_fecha ON Sincronizaciones(fecha);

-- Crear tabla de Sistemas Externos
DROP TABLE IF EXISTS Sistemas_Externos CASCADE;
CREATE TABLE Sistemas_Externos (
    id SERIAL PRIMARY KEY, -- Identificador único de la tabla Sistemas Externos
    guid UUID UNIQUE NOT NULL, -- GUID único para la tabla Sistemas Externos
    nombre VARCHAR(100) NOT NULL, -- Nombre del sistema externo
    url VARCHAR(255) NOT NULL -- URL del sistema externo
);
CREATE INDEX idx_sistemas_externos_nombre ON Sistemas_Externos(nombre);

-- Crear tabla de Reportes
DROP TABLE IF EXISTS Reportes CASCADE;
CREATE TABLE Reportes (
    id SERIAL PRIMARY KEY, -- Identificador único de la tabla Reportes
    guid UUID UNIQUE NOT NULL, -- GUID único para la tabla Reportes
    administrador_id INTEGER REFERENCES Usuarios(id) ON DELETE CASCADE, -- Referencia al administrador
    tipo_reporte VARCHAR(100) NOT NULL, -- Tipo de reporte
    fecha_generacion TIMESTAMP NOT NULL, -- Fecha y hora de generación del reporte
    detalles TEXT -- Detalles del reporte
);
CREATE INDEX idx_reportes_administrador_id ON Reportes(administrador_id);
CREATE INDEX idx_reportes_fecha_generacion ON Reportes(fecha_generacion);

-- Crear tabla de Estadísticas
DROP TABLE IF EXISTS Estadisticas CASCADE;
CREATE TABLE Estadisticas (
    id SERIAL PRIMARY KEY, -- Identificador único de la tabla Estadísticas
    guid UUID UNIQUE NOT NULL, -- GUID único para la tabla Estadísticas
    actividad_id INTEGER REFERENCES Actividades(id) ON DELETE CASCADE, -- Referencia a la actividad
    numero_inscritos INTEGER NOT NULL, -- Número de inscritos en la actividad
    numero_asistentes INTEGER NOT NULL, -- Número de asistentes a la actividad
    calificacion_promedio DECIMAL(2, 1) CHECK (calificacion_promedio >= 0 AND calificacion_promedio <= 5) -- Calificación promedio de la actividad
);
CREATE INDEX idx_estadisticas_actividad_id ON Estadisticas(actividad_id);
CREATE INDEX idx_estadisticas_numero_inscritos ON Estadisticas(numero_inscritos);
CREATE INDEX idx_estadisticas_numero_asistentes ON Estadisticas(numero_asistentes);

