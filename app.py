from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# Clave secreta necesaria para mostrar mensajes de éxito/error
app.secret_key = 'clave_secreta_colegio_insurgentes'

# --- CONFIGURACIÓN DE BASE DE DATOS (SQLite) ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///colegio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- MODELOS DE BASE DE DATOS ---
# Traducimos tu tabla 'alumnos' exacta a SQLAlchemy
class Alumno(db.Model):
    __tablename__ = 'alumnos'
    id_alumno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    matricula = db.Column(db.String(20), unique=True, nullable=False)
    nombres = db.Column(db.String(100), nullable=False)
    apellido_paterno = db.Column(db.String(100), nullable=False)
    apellido_materno = db.Column(db.String(100))
    curp = db.Column(db.String(18), unique=True, nullable=False)
    fecha_nacimiento = db.Column(db.String(20))
    genero = db.Column(db.String(1))
    
    # Datos del Tutor
    nombre_tutor = db.Column(db.String(100))
    telefono_tutor = db.Column(db.String(20))
    email_tutor = db.Column(db.String(100))
    
    # id_grupo = db.Column(db.Integer) # Lo conectaremos más adelante
    activo = db.Column(db.Boolean, default=True)


# --- RUTAS DE AUTENTICACIÓN ---
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def procesar_login():
    correo = request.form.get('correo')
    password = request.form.get('password')
    
    if correo == 'admin@colegioinsurgentes.edu.mx' and password == '123':
        return redirect(url_for('dashboard_admin'))
    elif correo == 'maestro@colegioinsurgentes.edu.mx' and password == '123':
        return redirect(url_for('dashboard_maestro'))
    else:
        return redirect(url_for('login'))

# --- RUTAS DEL SUPERADMIN ---
@app.route('/admin/dashboard')
def dashboard_admin():
    return render_template('admin/dashboard.html')

@app.route('/admin/registrar_alumno', methods=['GET', 'POST'])
def registrar_alumno():
    # Si el usuario presiona el botón de guardar (POST)
    if request.method == 'POST':
        try:
            nuevo_alumno = Alumno(
                matricula=request.form.get('matricula'),
                curp=request.form.get('curp'),
                nombres=request.form.get('nombres'),
                apellido_paterno=request.form.get('apellido_paterno'),
                apellido_materno=request.form.get('apellido_materno'),
                fecha_nacimiento=request.form.get('fecha_nacimiento'),
                genero=request.form.get('genero'),
                nombre_tutor=request.form.get('nombre_tutor'),
                telefono_tutor=request.form.get('telefono_tutor'),
                email_tutor=request.form.get('email_tutor')
            )
            # Guardamos en la base de datos
            db.session.add(nuevo_alumno)
            db.session.commit()
            flash('¡Alumno registrado exitosamente en el sistema!')
            return redirect(url_for('dashboard_admin'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar: Probablemente la Matrícula o CURP ya existen.')
            
    # Si solo está entrando a ver la página (GET)
    return render_template('admin/registrar_alumno.html')


# --- RUTAS DEL MAESTRO ---
@app.route('/maestro/dashboard')
def dashboard_maestro():
    return render_template('maestro/dashboard.html')

@app.route('/maestro/crear_actividad')
def crear_actividad():
    return render_template('maestro/crear_actividad.html')

if __name__ == '__main__':
    # Esto crea el archivo colegio.db y las tablas automáticamente al iniciar
    with app.app_context():
        db.create_all()
    app.run(debug=True)