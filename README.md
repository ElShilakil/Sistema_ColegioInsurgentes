# School Management System API

This project is a Flask-based REST API designed to manage students, teachers, groups, activities, and grades for an educational institution.

## Prerequisites

- Python 3.x
- PostgreSQL
- Required Libraries:
    - `Flask`
    - `psycopg2-binary`

## Installation

1. Clone the repository.
2. Install the dependencies using pip:
   ```bash
   pip install Flask psycopg2-binary
   ```

## Database Setup

Ensure you have a PostgreSQL database running and execute the necessary SQL scripts to create the tables for:
- Alumnos (Students)
- Maestros (Teachers)
- Grupos (Groups)
- Materias (Subjects)
- Periodos (Periods)
- Actividades (Activities)
- Calificaciones (Grades)

## Running the Application

To start the API server, run:
```bash
python app.py
```
The server will start at `http://localhost:5000`.

## API Documentation

For detailed information on available endpoints, request formats, and responses, please refer to the [API Documentation](Scripts%20para%20crear%20proyecto/api_docs.md).

### Quick Overview of Endpoints:
- `/api/alumnos`: Manage student records.
- `/api/maestros`: Manage teacher profiles.
- `/api/grupos`: Manage classroom groups.
- `/api/actividades`: Manage academic activities.
- `/api/calificaciones`: Manage student grades and feedback.
