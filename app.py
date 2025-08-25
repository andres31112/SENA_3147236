#IMPORTACIONES NECESARIAS
from flask import Flask
from flask_login import LoginManager
from controllers.models import db, Usuario, Rol, Permiso
from routes.auth import auth_bp
from routes.main import main_bp
from routes.admin import admin_bp
from config import Config

# --- INICIALIZACIÓN DE LA APP ---
app = Flask(__name__)

# --- CONFIGURACIÓN ---
app.config.from_object(Config)

db.init_app(app)

# --- CONFIGURACIÓN DE FLASK-LOGIN ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor, inicia sesión para acceder a esta página.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# --- FUNCIÓN DE INICIALIZACIÓN DE ROLES, PERMISOS Y SUPER ADMIN ---
def create_initial_data():
    with app.app_context():
        # Crear la base de datos y las tablas si no existen
        db.create_all()
        print("Base de datos y tablas verificadas/creadas.")

        # PERMISOS SUPER ADMIN
        permissions_to_create = {
            'gestion_usuarios': 'Acceso a la gestión de usuarios (CRUD)',
            'gestion_asignaturas': 'Acceso a la gestión de asignaturas',
            'registro_calificaciones': 'Acceso al registro y edición de calificaciones',
            'gestion_comunicados': 'Acceso a la gestión de comunicados',
            'gestion_inventario': 'Acceso a la gestión de inventario',
            'gestion_matriculas': 'Acceso a la gestión de matrículas',
            'gestion_electoral': 'Acceso a la gestión electoral',
            'crear_roles': 'Permiso para crear roles',
            'ver_roles': 'Permiso para ver roles',
            'editar_roles': 'Permiso para editar roles',
            'eliminar_roles': 'Permiso para eliminar roles'
        }
        
        for name, desc in permissions_to_create.items():
            if not Permiso.query.filter_by(nombre_permiso=name).first():
                new_permission = Permiso(nombre_permiso=name, descripcion=desc)
                db.session.add(new_permission)
                print(f"Permiso '{name}' creado.")
        db.session.commit()

        # ROLES BÁSICOS
        roles_to_create = ['Super Admin', 'Profesor', 'Estudiante', 'Usuario Estándar']
        for role_name in roles_to_create:
            if not Rol.query.filter_by(nombre_rol=role_name).first():
                if role_name == 'Super Admin':
                    # Asigna todos los permisos al rol de 'Super Admin'
                    all_permissions = Permiso.query.all()
                    super_admin_role = Rol(nombre_rol='Super Admin', descripcion='Administrador con todos los permisos')
                    super_admin_role.permisos = all_permissions
                    db.session.add(super_admin_role)
                    print("Rol 'Super Admin' creado con todos los permisos.")
                elif role_name == 'Profesor':
                    teacher_role = Rol(nombre_rol='Profesor', descripcion='Acceso a funciones docentes')
                    db.session.add(teacher_role)
                    print("Rol 'Profesor' creado.")
                elif role_name == 'Estudiante':
                    student_role = Rol(nombre_rol='Estudiante', descripcion='Acceso a funciones estudiantiles')
                    db.session.add(student_role)
                    print("Rol 'Estudiante' creado.")
                elif role_name == 'Usuario Estándar':
                    default_role = Rol(nombre_rol='Usuario Estándar', descripcion='Rol por defecto para usuarios sin rol específico.')
                    db.session.add(default_role)
                    print("Rol 'Usuario Estándar' creado.")
        db.session.commit()

        # USUARIO SUPERADMIN
        if not Usuario.query.filter_by(numero_identidad='000000000').first():
            super_admin_role = Rol.query.filter_by(nombre_rol='Super Admin').first()
            if super_admin_role:
                super_admin = Usuario(
                    numero_identidad='000000000',
                    tipo_documento='cc',
                    nombre_completo='Super Administrador',
                    correo_electronico='superadmin@institucion.com',
                    telefono_celular='3001234567',
                    estado_cuenta='activa',
                    rol_obj=super_admin_role
                )
                super_admin.set_password('admin123')
                db.session.add(super_admin)
                db.session.commit()
                print("Usuario 'Super Administrador' creado con contraseña 'admin123'.")
            else:
                print("Rol 'Super Admin' no encontrado. No se pudo crear el usuario superadmin.")


app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)

if __name__ == '__main__':
    with app.app_context():
        create_initial_data()
    app.run(debug=True)