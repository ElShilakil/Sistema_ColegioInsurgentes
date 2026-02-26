-- Formative Fields
INSERT INTO cat_campos_formativos (nombre_campo) VALUES 
('Lenguajes'), 
('Saberes y Pensamiento Científico'),
('Ética, Naturaleza y Sociedades'), 
('De lo humano y lo comunitario');

-- Teachers
INSERT INTO usuarios_maestros (nombre_completo, correo, password_hash) VALUES 
('Roberto Gómez', 'roberto.gomez@cinsurgentes.edu.mx', 'hash_p@ss123'),
('Ana Martínez', 'ana.mtz@cinsurgentes.edu.mx', 'hash_secure456');

-- Evaluation Periods
INSERT INTO periodos_evaluacion (nombre_periodo, fecha_inicio, fecha_fin, ciclo_escolar) VALUES 
('Primer Trimestre', '2025-09-01', '2025-11-30', '2025-2026');

-- Subjects
INSERT INTO materias (nombre_materia, id_campo_relacionado, grado_sugerido) VALUES 
('Matemáticas I', 2, 1),
('Español I', 1, 1);

-- Groups (Linking Teacher 1 to 1st Grade Section A)
INSERT INTO grupos (grado, grupo, ciclo_escolar, id_maestro_titular) VALUES 
(1, 'A', '2025-2026', 1);

-- Students
INSERT INTO alumnos (matricula, nombres, apellido_paterno, curp, id_grupo) VALUES 
('AL2025001', 'Juan', 'Pérez', 'PERJ010101HDFRRS01', 1);

-- Activities
INSERT INTO actividades (titulo, descripcion, tipo_actividad, porcentaje_valor, id_periodo, id_materia, id_grupo, id_maestro) VALUES 
('Examen Parcial 1', 'Evaluación de álgebra básica', 'Examen', 40, 1, 1, 1, 1);

-- Grades
INSERT INTO calificaciones (id_actividad, id_alumno, calificacion, retroalimentacion) VALUES 
(1, 1, 8.5, 'Buen desempeño, revisar ecuaciones de primer grado.');

SELECT 
    a.nombres, 
    m.nombre_materia, 
    act.titulo as actividad, 
    c.calificacion
FROM calificaciones c
JOIN alumnos a ON c.id_alumno = a.id_alumno
JOIN actividades act ON c.id_actividad = act.id_actividad
JOIN materias m ON act.id_materia = m.id_material;