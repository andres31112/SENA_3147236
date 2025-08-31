#IMPORTACIONES NECESARIAS
from flask import Flask
from flask_login import LoginManager
from controllers.models import db, Usuario, Rol, Permiso
from routes.auth import auth_bp
from routes.main import main_bp
from routes.admin import admin_bp
from routes.estudiantes import estudiante_bp
from routes.profesor import profesor_bp
from routes.padres import padre_bp
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

        # PERMISOS POR ROL
        permissions_for_roles = {
            'Super Admin': [
                'gestion_usuarios', 'gestion_asignaturas', 'registro_calificaciones',
                'gestion_comunicados', 'gestion_inventario', 'gestion_matriculas',
                'gestion_electoral', 'crear_roles', 'ver_roles', 'editar_roles',
                'eliminar_roles'
            ],
            'Profesor': [
                'ver_calificaciones_propias', 'ver_horario_clases', 'ver_lista_estudiantes',
                'registrar_calificaciones', 'gestion_comunicados_profesor'
            ],
            'Estudiante': [
                'ver_calificaciones', 'ver_horario', 'ver_historial_academico',
                'inscripcion_materias', 'ver_comunicaciones_estudiante', 'ver_estado_cuenta',
                'editar_perfil', 'acceso_soporte'
            ],
            'Padre': [
                'ver_calificaciones_hijo', 'ver_horario_hijo', 'ver_comunicaciones_padre',
                'acceso_soporte'
            ],
        }

        # CREAR TODOS LOS PERMISOS
        all_permissions_to_create = set()
        for perms in permissions_for_roles.values():
            all_permissions_to_create.update(perms)
        
        for name in all_permissions_to_create:
            if not Permiso.query.filter_by(nombre_permiso=name).first():
                new_permission = Permiso(nombre_permiso=name, descripcion=f"Permiso para '{name}'")
                db.session.add(new_permission)
                print(f"Permiso '{name}' creado.")
        db.session.commit()

        # CREAR Y ASIGNAR PERMISOS A LOS ROLES
        roles_to_create = ['Super Admin', 'Profesor', 'Estudiante', 'Padre']
        for role_name in roles_to_create:
            role = Rol.query.filter_by(nombre_rol=role_name).first()
            if not role:
                role = Rol(nombre_rol=role_name, descripcion=f"Rol de {role_name}")
                db.session.add(role)
                db.session.commit() # Necesario para obtener el ID del rol

            # Asignar permisos al rol
            role_permissions = [Permiso.query.filter_by(nombre_permiso=name).first() 
                                for name in permissions_for_roles.get(role_name, [])]
            role.permisos = role_permissions
            db.session.commit()
            print(f"Permisos asignados al rol '{role_name}'.")

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
app.register_blueprint(estudiante_bp)
app.register_blueprint(padre_bp)
app.register_blueprint(profesor_bp)

if __name__ == '__main__':
    with app.app_context():
        create_initial_data()
    app.run(debug=True)