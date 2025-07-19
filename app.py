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
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')
    
#-------RUTAS ADMIN-------    
@app.route('/PANEL_ADMIN')
def gestion():
    return render_template('superadmin/gestion_usuarios/dashboard.html')
@app.route('/inicio')
def inicio():
    return render_template('superadmin/inicio/inicio.html')

#-------RUTAS GESTION INCENTARIO-------
@app.route('/Gestion_Inventario')
def gestion_i():
    return render_template('superadmin/gestion_inventario/gi.html')

@app.route('/Equipos')
def equipos():
    return render_template('superadmin/gestion_inventario/equipos.html')

@app.route('/Registro_Equipo')
def registro_equipo():
    return render_template('superadmin/gestion_inventario/registro_equipo.html')

#------RUTAS GESTION USUARIOS/ROLES------
@app.route('/Profesores')
def Profesores():
    return render_template('superadmin/gestion_usuarios/profesores.html')

@app.route('/crear_rol')
def crear_rol():
    return render_template('superadmin/gestion_usuarios/crear_rol.html')

@app.route('/lista_rol')
def lista_rol():
    return render_template('superadmin/gestion_usuarios/lista_rol.html')

@app.route('/editar_rol')
def editar_rol():
    return render_template('superadmin/gestion_usuarios/editar_rol.html')

@app.route('/crear_usuario')
def crear_usuario():
    return render_template('superadmin/gestion_usuarios/crear_usuario.html')

if __name__ == '__main__':
    app.run(debug=True)