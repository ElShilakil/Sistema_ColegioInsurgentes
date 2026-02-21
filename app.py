from flask import Flask, render_template, request

app = Flask(__name__)

# Ruta principal que muestra el Login
@app.route('/')
def login():
    # Flask busca automáticamente en la carpeta 'templates'
    return render_template('login.html')

# Ruta para procesar el formulario (la dejaremos preparada para después)
@app.route('/login', methods=['POST'])
def procesar_login():
    correo = request.form.get('correo')
    password = request.form.get('password')
    # Aquí irá la lógica de validación con la base de datos más adelante
    return f"Intento de acceso con: {correo}"

if __name__ == '__main__':
    # debug=True permite que los cambios se reflejen sin reiniciar el servidor
    app.run(debug=True)