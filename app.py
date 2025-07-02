# --- IMPORTACIONES ---
# Añadimos las importaciones necesarias de flask_login
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from basesdatos.models import db, Usuario # Asumo que tu archivo de modelos se llama así

# --- INICIALIZACIÓN DE LA APP ---
app = Flask(__name__)

# --- CONFIGURACIÓN ---
# 1. Configuración de la Base de Datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1:3306/institucion_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 2. SECRET_KEY para que flash() y las sesiones de login funcionen
app.config['SECRET_KEY'] = 'una-llave-secreta-para-proteger-las-sesiones'

# 3. Inicializar la base de datos con la app
db.init_app(app)

# --- [PASO 1] CONFIGURACIÓN DE FLASK-LOGIN ---
login_manager = LoginManager()
login_manager.init_app(app)
# Si un usuario no logueado intenta ir a una página protegida, lo redirige aquí
login_manager.login_view = 'login' 
login_manager.login_message = 'Por favor, inicia sesión para acceder a esta página.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    """Carga el usuario desde la base de datos para mantener la sesión."""
    return Usuario.query.get(int(user_id))

# --- RUTAS PÚBLICAS ---
@app.route('/')
def index():
    # Ahora la página principal puede saber si el usuario está logueado o no
    return render_template('index.html')

# --- [PASO 2] RUTA DE LOGIN CON LÓGICA GET Y POST ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Si el usuario ya tiene una sesión activa, lo mandamos al dashboard
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    # Si el método es POST, el usuario ha enviado el formulario
    if request.method == 'POST':
        correo = request.form.get('correo_electronico')
        password = request.form.get('password')

        # Buscamos al usuario en la base de datos
        usuario = Usuario.query.filter_by(correo_electronico=correo).first()

        # Verificamos si el usuario existe y la contraseña es correcta
        if usuario and usuario.check_password(password):
            # Si es correcto, iniciamos la sesión
            login_user(usuario)
            flash('Inicio de sesión exitoso.', 'success')
            # Redirigimos al panel del usuario
            return redirect(url_for('dashboard'))
        else:
            # Si no, mostramos un error
            flash('Credenciales incorrectas. Por favor, verifica tu correo y contraseña.', 'danger')
            return redirect(url_for('login'))

    # Si el método es GET, simplemente mostramos la página de login
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)