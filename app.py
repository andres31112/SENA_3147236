# ===============================
# IMPORTACIONES NECESARIAS
# ===============================
from flask import Flask
from flask_login import LoginManager
from controllers.models import db, Usuario, Rol
from routes.auth import auth_bp
from routes.main import main_bp
from routes.admin import admin_bp
from routes.estudiantes import estudiante_bp
from routes.profesor import profesor_bp
from routes.padres import padre_bp
from config import Config
from extensions import init_app # Importa la función de inicialización

# ===============================
# INICIALIZACIÓN DE LA APP
# ===============================
app = Flask(__name__)
app.config.from_object(Config)
init_app(app) # <-- ¡CAMBIO IMPORTANTE AQUÍ!

# ===============================
# CONFIGURACIÓN DE FLASK-LOGIN
# ===============================
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor, inicia sesión para acceder a esta página.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# ===============================
# CREACIÓN DE DATOS INICIALES
# ===============================
def create_initial_data():
    with app.app_context():
        db.create_all()
        print("Base de datos y tablas verificadas/creadas.")

        # Roles a crear
        roles_to_create = ['Super Admin', 'Profesor', 'Estudiante', 'Padre']

        for role_name in roles_to_create:
            role = Rol.query.filter_by(nombre=role_name).first()
            if not role:
                role = Rol(nombre=role_name)
                db.session.add(role)
                db.session.commit()
                print(f"Rol '{role_name}' creado.")

        # Crear superadmin si no existe
        if not Usuario.query.filter_by(no_identidad='000000000').first():
            super_admin_role = Rol.query.filter_by(nombre='Super Admin').first()
            if super_admin_role:
                super_admin = Usuario(
                    no_identidad='000000000',
                    tipo_doc='CC',
                    nombre='Super',
                    apellido='Administrador',
                    correo='superadmin@institucion.com',
                    telefono='3001234567',
                    direccion='',
                    id_rol_fk=super_admin_role.id_rol
                )
                super_admin.set_password('admin123')
                db.session.add(super_admin)
                db.session.commit()
                print("Usuario 'Super Administrador' creado con contraseña 'admin123'.")
            else:
                print("Rol 'Super Admin' no encontrado. No se pudo crear el usuario superadmin.")

# ===============================
# REGISTRO DE BLUEPRINTS
# ===============================
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(estudiante_bp)
app.register_blueprint(padre_bp)
app.register_blueprint(profesor_bp)

# ===============================
# EJECUCIÓN
# ===============================
if __name__ == '__main__':
    with app.app_context():
        create_initial_data()
    app.run(debug=True)