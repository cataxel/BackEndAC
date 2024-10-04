-- Vista para la tabla Roles
CREATE OR REPLACE VIEW vista_roles AS
SELECT
    guid AS id,
    nombre,
    descripcion
FROM Roles;

-- Vista para la tabla Usuarios
CREATE OR REPLACE VIEW vista_usuarios AS
SELECT
    guid AS id,
    nombre,
    correo,
    contraseña,
    rol_id
FROM Usuarios;

-- Vista para la tabla Perfiles
CREATE OR REPLACE VIEW vista_perfiles AS
SELECT
    guid AS id,
    usuario_id,
    telefono,
    direccion,
    preferencias
FROM Perfiles;

-- Vista para la tabla Sesiones
CREATE OR REPLACE VIEW vista_sesiones AS
SELECT
    guid AS id,
    usuario_id,
    fecha_inicio,
    fecha_fin
FROM Sesiones;

-- Vista para la tabla Actividades
CREATE OR REPLACE VIEW vista_actividades AS
SELECT
    guid AS id,
    nombre,
    descripcion,
    fecha_inicio,
    fecha_fin,
    capacidad
FROM Actividades;

-- Vista para la tabla Asistencia
CREATE OR REPLACE VIEW vista_asistencia AS
SELECT
    guid AS id,
    usuario_id,
    actividad_id,
    fecha_registro,
    estado
FROM Asistencia;

-- Vista para la tabla Inscripciones
CREATE OR REPLACE VIEW vista_inscripciones AS
SELECT
    guid AS id,
    usuario_id,
    actividad_id,
    fecha_inscripcion,
    estado
FROM Inscripciones;

-- Vista para la tabla Listas de Espera
CREATE OR REPLACE VIEW vista_listas_espera AS
SELECT
    guid AS id,
    usuario_id,
    actividad_id,
    fecha_registro
FROM Listas_Espera;

-- Vista para la tabla Evaluaciones
CREATE OR REPLACE VIEW vista_evaluaciones AS
SELECT
    guid AS id,
    usuario_id,
    actividad_id,
    calificacion,
    comentarios
FROM Evaluaciones;

-- Vista para la tabla Participaciones
CREATE OR REPLACE VIEW vista_participaciones AS
SELECT
    guid AS id,
    usuario_id,
    actividad_id,
    fecha_participacion
FROM Participaciones;

-- Vista para la tabla Notificaciones
CREATE OR REPLACE VIEW vista_notificaciones AS
SELECT
    guid AS id,
    usuario_id,
    asunto,
    mensaje,
    fecha_envio
FROM Notificaciones;

-- Vista para la tabla Anuncios
CREATE OR REPLACE VIEW vista_anuncios AS
SELECT
    guid AS id,
    administrador_id,
    titulo,
    contenido,
    fecha_publicacion
FROM Anuncios;

-- Vista para la tabla Sincronizaciones
CREATE OR REPLACE VIEW vista_sincronizaciones AS
SELECT
    guid AS id,
    fecha,
    estado,
    detalles
FROM Sincronizaciones;

-- Vista para la tabla Sistemas Externos
CREATE OR REPLACE VIEW vista_sistemas_externos AS
SELECT
    guid AS id,
    nombre,
    url
FROM Sistemas_Externos;

-- Vista para la tabla Reportes
CREATE OR REPLACE VIEW vista_reportes AS
SELECT
    guid AS id,
    administrador_id,
    tipo_reporte,
    fecha_generacion,
    detalles
FROM Reportes;

-- Vista para la tabla Estadísticas
CREATE OR REPLACE VIEW vista_estadisticas AS
SELECT
    guid AS id,
    actividad_id,
    numero_inscritos,
    numero_asistentes,
    calificacion_promedio
FROM Estadisticas;