-- Database: colegio_insurgentes

-- DROP DATABASE IF EXISTS "colegio_insurgentes";

CREATE DATABASE "colegio_insurgentes"
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

COMMENT ON DATABASE "AlumnoControl"
    IS 'Base de datos para el sistema de control escolar, gestionando alumnos, maestros, materias, actividades y calificaciones.';

CREATE TYPE tipo_actividad_enum AS ENUM ('Tarea', 'Examen', 'Actividad');

CREATE TABLE cat_campos_formativos (
    id_campo SERIAL PRIMARY KEY,
    nombre_campo VARCHAR(255) NOT NULL
);

-- Evaluation periods
CREATE TABLE periodos_evaluacion (
    id_periodo SERIAL PRIMARY KEY,
    nombre_periodo VARCHAR(100) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    ciclo_escolar VARCHAR(20) NOT NULL,
    activo BOOLEAN DEFAULT TRUE
);

-- Teacher users
CREATE TABLE usuarios_maestros (
    id_maestro SERIAL PRIMARY KEY,
    nombre_completo VARCHAR(255) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL CHECK (correo ~ '^[A-Za-z0-9._-]+@cinsurgentes\.edu\.mx$'),   
    password_hash VARCHAR(255) NOT NULL,
    activo BOOLEAN DEFAULT TRUE
);

-- Subjects
CREATE TABLE materias (
    id_material SERIAL PRIMARY KEY,
    nombre_materia VARCHAR(150) NOT NULL,
    id_campo_relacionado INT REFERENCES cat_campos_formativos(id_campo),
    grado_sugerido INT
);

-- Groups
CREATE TABLE grupos (
    id_grupo SERIAL PRIMARY KEY,
    grado INT NOT NULL,
    grupo CHAR(1) NOT NULL,
    ciclo_escolar VARCHAR(20) NOT NULL,
    id_maestro_titular INT REFERENCES usuarios_maestros(id_maestro)
);

-- Students
CREATE TABLE alumnos (
    id_alumno SERIAL PRIMARY KEY,
    matricula VARCHAR(50) UNIQUE NOT NULL,
    nombres VARCHAR(100) NOT NULL,
    apellido_paterno VARCHAR(100) NOT NULL,
    apellido_materno VARCHAR(100),
    curp VARCHAR(18) UNIQUE,
    fecha_nacimiento DATE,
    genero CHAR(1),
    nombre_tutor VARCHAR(255),
    telefono_tutor VARCHAR(20),
    email_tutor VARCHAR(100),
    id_grupo INT REFERENCES grupos(id_grupo),
    activo BOOLEAN DEFAULT TRUE
);

-- Activities
CREATE TABLE actividades (
    id_actividad SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT,
    fecha_entrega TIMESTAMP,
    tipo_actividad tipo_actividad_enum,
    porcentaje_valor INT,
    id_periodo INT REFERENCES periodos_evaluacion(id_periodo),
    id_materia INT REFERENCES materias(id_material),
    id_grupo INT REFERENCES grupos(id_grupo),
    id_maestro INT REFERENCES usuarios_maestros(id_maestro),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Grades/Qualifications
CREATE TABLE calificaciones (
    id_calificacion SERIAL PRIMARY KEY,
    id_actividad INT REFERENCES actividades(id_actividad) ON DELETE CASCADE,
    id_alumno INT REFERENCES alumnos(id_alumno) ON DELETE CASCADE,
    calificacion DECIMAL(4,2),
    retroalimentacion TEXT,
    fecha_capture TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

