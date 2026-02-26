# School Management System API Documentation

**Base URL:** `http://localhost:5000/api`  
**Content-Type:** `application/json`

---

## 1. Alumnos (Students)

### `GET /alumnos`
* **Description:** Retrieves all active students.
* **Response:** `200 OK` (Array of student objects)

### `GET /alumnos/<id>`
* **Description:** Retrieves a specific active student by their ID.
* **Response:** `200 OK` (Single student object) or `404 Not Found`

### `POST /alumnos`
* **Description:** Creates a new student record.
* **Request Body:**
    ```json
    {
      "matricula": "AL2025001",
      "nombres": "Juan",
      "apellido_paterno": "Perez",
      "apellido_materno": "Gomez", 
      "curp": "PERJ010101HDFRRS01", 
      "id_grupo": 1
    }
    ```
    *(Note: `apellido_materno` and `curp` are optional)*
* **Response:** `201 Created`

### `PUT /alumnos/<id>`
* **Description:** Updates an existing student's information.
* **Request Body:** Same fields as `POST /alumnos` (excluding `matricula` and `curp`).
* **Response:** `200 OK`

### `DELETE /alumnos/<id>`
* **Description:** Soft deletes a student (sets `activo = FALSE`).
* **Response:** `200 OK`

---

## 2. Actividades (Activities)

### `GET /actividades`
* **Description:** Retrieves all academic activities.
* **Response:** `200 OK`

### `GET /actividades/<id>`
* **Description:** Retrieves a specific activity by its ID.
* **Response:** `200 OK` or `404 Not Found`

### `POST /actividades`
* **Description:** Creates a new activity.
* **Request Body:**
    ```json
    {
      "titulo": "Examen Parcial 1",
      "descripcion": "Evaluacion de algebra",
      "tipo_actividad": "Examen",
      "porcentaje_valor": 40,
      "id_periodo": 1,
      "id_materia": 1,
      "id_grupo": 1,
      "id_maestro": 1
    }
    ```
* **Response:** `201 Created`

### `PUT /actividades/<id>`
* **Description:** Updates an activity's core details.
* **Request Body:** Requires `titulo`, `descripcion`, and `porcentaje_valor`.
* **Response:** `200 OK`

### `DELETE /actividades/<id>`
* **Description:** Permanently deletes an activity.
* **Response:** `200 OK`

---

## 3. Calificaciones (Grades)

### `GET /calificaciones`
* **Description:** Retrieves all grade records.
* **Response:** `200 OK`

### `GET /calificaciones/<id>`
* **Description:** Retrieves a specific grade record by ID.
* **Response:** `200 OK` or `404 Not Found`

### `POST /calificaciones`
* **Description:** Assigns a grade to a student for a specific activity.
* **Request Body:**
    ```json
    {
      "id_actividad": 1,
      "id_alumno": 1,
      "calificacion": 8.5,
      "retroalimentacion": "Buen trabajo."
    }
    ```
* **Response:** `201 Created`

### `PUT /calificaciones/<id>`
* **Description:** Updates an existing grade or feedback.
* **Request Body:** Requires `calificacion` and `retroalimentacion`.
* **Response:** `200 OK`

### `DELETE /calificaciones/<id>`
* **Description:** Permanently deletes a grade record.
* **Response:** `200 OK`

---

## 4. Maestros (Teachers)

### `GET /maestros`
* **Description:** Retrieves all active teachers (excludes password hashes for security).
* **Response:** `200 OK`

### `POST /maestros`
* **Description:** Creates a new teacher profile.
* **Request Body:**
    ```json
    {
      "nombre_completo": "Ana Martinez",
      "correo": "ana.mtz@escuela.edu",
      "password_hash": "hashed_string_here"
    }
    ```
* **Response:** `201 Created`

### `PUT /maestros/<id>`
* **Description:** Updates a teacher's name or email.
* **Request Body:** Requires `nombre_completo` and `correo`.
* **Response:** `200 OK`

### `DELETE /maestros/<id>`
* **Description:** Soft deletes a teacher profile (sets `activo = FALSE`).
* **Response:** `200 OK`

---

## 5. Grupos (Groups)

### `GET /grupos`
* **Description:** Retrieves all classroom groups.
* **Response:** `200 OK`

### `POST /grupos`
* **Description:** Creates a new group.
* **Request Body:**
    ```json
    {
      "grado": 1,
      "grupo": "A",
      "ciclo_escolar": "2025-2026",
      "id_maestro_titular": 1
    }
    ```
* **Response:** `201 Created`

### `PUT /grupos/<id>`
* **Description:** Updates the assigned teacher (`id_maestro_titular`) for a group.
* **Request Body:** Requires `id_maestro_titular`.
* **Response:** `200 OK`

### `DELETE /grupos/<id>`
* **Description:** Permanently deletes a group.
* **Response:** `200 OK`