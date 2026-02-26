from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Replace these with your actual database credentials
DB_CONFIG = {
    "dbname": "AlumnoControl",
    "user": "postgres",
    "password": "1995",
    "host": "localhost",
    "port": "5432"
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

CORS(app)

def execute_db(query, params=(), fetch=True, commit=False):
    """Helper function to execute database queries safely."""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute(query, params)
        result = cur.fetchall() if fetch else None
        if commit:
            conn.commit()
        return result, None
    except Exception as e:
        conn.rollback()
        return None, str(e)
    finally:
        cur.close()
        conn.close()

# ==========================================
# ALUMNOS (Students) CRUD
# ==========================================

@app.route('/api/alumnos', methods=['GET'])
def get_alumnos():
    res, err = execute_db("SELECT * FROM alumnos WHERE activo = TRUE;")
    return jsonify({"error": err} if err else res), 500 if err else 200

@app.route('/api/alumnos/<int:id>', methods=['GET'])
def get_alumno(id):
    res, err = execute_db("SELECT * FROM alumnos WHERE id_alumno = %s AND activo = TRUE;", (id,))
    if err: return jsonify({"error": err}), 500
    return jsonify(res[0] if res else {"message": "Not found"}), 200 if res else 404

@app.route('/api/alumnos', methods=['POST'])
def create_alumno():
    data = request.get_json()
    query = """
        INSERT INTO alumnos (matricula, nombres, apellido_paterno, apellido_materno, curp, id_grupo) 
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING *;
    """
    params = (data['matricula'], data['nombres'], data['apellido_paterno'], data.get('apellido_materno'), data.get('curp'), data['id_grupo'])
    res, err = execute_db(query, params, fetch=True, commit=True)
    return jsonify({"error": err} if err else res[0]), 500 if err else 201

@app.route('/api/alumnos/<int:id>', methods=['PUT'])
def update_alumno(id):
    data = request.get_json()
    query = """
        UPDATE alumnos SET nombres = %s, apellido_paterno = %s, apellido_materno = %s, id_grupo = %s 
        WHERE id_alumno = %s RETURNING *;
    """
    params = (data['nombres'], data['apellido_paterno'], data.get('apellido_materno'), data['id_grupo'], id)
    res, err = execute_db(query, params, fetch=True, commit=True)
    return jsonify({"error": err} if err else res[0]), 500 if err else 200

@app.route('/api/alumnos/<int:id>', methods=['DELETE'])
def delete_alumno(id):
    # Soft delete
    res, err = execute_db("UPDATE alumnos SET activo = FALSE WHERE id_alumno = %s RETURNING id_alumno;", (id,), fetch=True, commit=True)
    return jsonify({"error": err} if err else {"message": "Deleted successfully"}), 500 if err else 200


# ==========================================
# ACTIVIDADES (Activities) CRUD
# ==========================================

@app.route('/api/actividades', methods=['GET'])
def get_actividades():
    res, err = execute_db("SELECT * FROM actividades;")
    return jsonify({"error": err} if err else res), 500 if err else 200

@app.route('/api/actividades/<int:id>', methods=['GET'])
def get_actividad(id):
    res, err = execute_db("SELECT * FROM actividades WHERE id_actividad = %s;", (id,))
    if err: return jsonify({"error": err}), 500
    return jsonify(res[0] if res else {"message": "Not found"}), 200 if res else 404

@app.route('/api/actividades', methods=['POST'])
def create_actividad():
    data = request.get_json()
    query = """
        INSERT INTO actividades (titulo, descripcion, tipo_actividad, porcentaje_valor, id_periodo, id_materia, id_grupo, id_maestro)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;
    """
    params = (data['titulo'], data.get('descripcion'), data['tipo_actividad'], data['porcentaje_valor'], data['id_periodo'], data['id_materia'], data['id_grupo'], data['id_maestro'])
    res, err = execute_db(query, params, fetch=True, commit=True)
    return jsonify({"error": err} if err else res[0]), 500 if err else 201

@app.route('/api/actividades/<int:id>', methods=['PUT'])
def update_actividad(id):
    data = request.get_json()
    query = """
        UPDATE actividades SET titulo = %s, descripcion = %s, porcentaje_valor = %s 
        WHERE id_actividad = %s RETURNING *;
    """
    params = (data['titulo'], data.get('descripcion'), data['porcentaje_valor'], id)
    res, err = execute_db(query, params, fetch=True, commit=True)
    return jsonify({"error": err} if err else res[0]), 500 if err else 200

@app.route('/api/actividades/<int:id>', methods=['DELETE'])
def delete_actividad(id):
    res, err = execute_db("DELETE FROM actividades WHERE id_actividad = %s RETURNING id_actividad;", (id,), fetch=True, commit=True)
    return jsonify({"error": err} if err else {"message": "Deleted successfully"}), 500 if err else 200


# ==========================================
# CALIFICACIONES (Grades) CRUD
# ==========================================

@app.route('/api/calificaciones', methods=['GET'])
def get_calificaciones():
    res, err = execute_db("SELECT * FROM calificaciones;")
    return jsonify({"error": err} if err else res), 500 if err else 200

@app.route('/api/calificaciones/<int:id>', methods=['GET'])
def get_calificacion(id):
    res, err = execute_db("SELECT * FROM calificaciones WHERE id_calificacion = %s;", (id,))
    if err: return jsonify({"error": err}), 500
    return jsonify(res[0] if res else {"message": "Not found"}), 200 if res else 404

@app.route('/api/calificaciones', methods=['POST'])
def create_calificacion():
    data = request.get_json()
    query = "INSERT INTO calificaciones (id_actividad, id_alumno, calificacion, retroalimentacion) VALUES (%s, %s, %s, %s) RETURNING *;"
    params = (data['id_actividad'], data['id_alumno'], data['calificacion'], data.get('retroalimentacion'))
    res, err = execute_db(query, params, fetch=True, commit=True)
    return jsonify({"error": err} if err else res[0]), 500 if err else 201

@app.route('/api/calificaciones/<int:id>', methods=['PUT'])
def update_calificacion(id):
    data = request.get_json()
    query = "UPDATE calificaciones SET calificacion = %s, retroalimentacion = %s WHERE id_calificacion = %s RETURNING *;"
    params = (data['calificacion'], data.get('retroalimentacion'), id)
    res, err = execute_db(query, params, fetch=True, commit=True)
    return jsonify({"error": err} if err else res[0]), 500 if err else 200

@app.route('/api/calificaciones/<int:id>', methods=['DELETE'])
def delete_calificacion(id):
    res, err = execute_db("DELETE FROM calificaciones WHERE id_calificacion = %s RETURNING id_calificacion;", (id,), fetch=True, commit=True)
    return jsonify({"error": err} if err else {"message": "Deleted successfully"}), 500 if err else 200


# ==========================================
# MAESTROS (Teachers) CRUD
# ==========================================

@app.route('/api/maestros', methods=['GET'])
def get_maestros():
    res, err = execute_db("SELECT id_maestro, nombre_completo, correo, activo FROM usuarios_maestros WHERE activo = TRUE;")
    return jsonify({"error": err} if err else res), 500 if err else 200

@app.route('/api/maestros', methods=['POST'])
def create_maestro():
    data = request.get_json()
    query = "INSERT INTO usuarios_maestros (nombre_completo, correo, password_hash) VALUES (%s, %s, %s) RETURNING id_maestro, nombre_completo, correo;"
    res, err = execute_db(query, (data['nombre_completo'], data['correo'], data['password_hash']), fetch=True, commit=True)
    return jsonify({"error": err} if err else res[0]), 500 if err else 201

@app.route('/api/maestros/<int:id>', methods=['PUT'])
def update_maestro(id):
    data = request.get_json()
    query = "UPDATE usuarios_maestros SET nombre_completo = %s, correo = %s WHERE id_maestro = %s RETURNING id_maestro, nombre_completo, correo;"
    res, err = execute_db(query, (data['nombre_completo'], data['correo'], id), fetch=True, commit=True)
    return jsonify({"error": err} if err else res[0]), 500 if err else 200

@app.route('/api/maestros/<int:id>', methods=['DELETE'])
def delete_maestro(id):
    res, err = execute_db("UPDATE usuarios_maestros SET activo = FALSE WHERE id_maestro = %s RETURNING id_maestro;", (id,), fetch=True, commit=True)
    return jsonify({"error": err} if err else {"message": "Deleted successfully"}), 500 if err else 200


# ==========================================
# GRUPOS (Groups) CRUD
# ==========================================

@app.route('/api/grupos', methods=['GET'])
def get_grupos():
    res, err = execute_db("SELECT * FROM grupos;")
    return jsonify({"error": err} if err else res), 500 if err else 200

@app.route('/api/grupos', methods=['POST'])
def create_grupo():
    data = request.get_json()
    query = "INSERT INTO grupos (grado, grupo, ciclo_escolar, id_maestro_titular) VALUES (%s, %s, %s, %s) RETURNING *;"
    res, err = execute_db(query, (data['grado'], data['grupo'], data['ciclo_escolar'], data['id_maestro_titular']), fetch=True, commit=True)
    return jsonify({"error": err} if err else res[0]), 500 if err else 201

@app.route('/api/grupos/<int:id>', methods=['PUT'])
def update_grupo(id):
    data = request.get_json()
    query = "UPDATE grupos SET id_maestro_titular = %s WHERE id_grupo = %s RETURNING *;"
    res, err = execute_db(query, (data['id_maestro_titular'], id), fetch=True, commit=True)
    return jsonify({"error": err} if err else res[0]), 500 if err else 200

@app.route('/api/grupos/<int:id>', methods=['DELETE'])
def delete_grupo(id):
    res, err = execute_db("DELETE FROM grupos WHERE id_grupo = %s RETURNING id_grupo;", (id,), fetch=True, commit=True)
    return jsonify({"error": err} if err else {"message": "Deleted successfully"}), 500 if err else 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)