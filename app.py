# IMPORTACIONES NECESARIAS
from flask import Flask, render_template, request, jsonify
from flask_login import LoginManager
from datetime import datetime

# MODELOS Y DB
from controllers.models import db, Usuario, Rol, Permiso, Comunicado,Evento

# BLUEPRINTS
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

# --- RUTAS ---
@app.route('/')
def index():
    usuario = Usuario.query.first()  # Usuario logueado ejemplo
    return render_template('index.html', usuario=usuario)

@app.route('/mensajes/<int:id_usuario>')
def inbox(id_usuario):
    # Bandeja de entrada
    mensajes = Comunicado.query.filter_by(IdUsuarioDestinatario=id_usuario, Eliminado=False).all()
    result = []
    for m in mensajes:
        result.append({
            'Id': m.Id,
            'Mensaje': m.Mensaje,
            'FechaHora': m.FechaHora.strftime("%Y-%m-%d %H:%M"),
            'nombre_rem': m.remitente.nombre_completo if m.remitente else 'Desconocido'
        })
    return jsonify(result)

@app.route('/enviados/<int:id_usuario>')
def enviados(id_usuario):
    # Bandeja de enviados
    mensajes = Comunicado.query.filter_by(IdUsuarioRemitente=id_usuario, Eliminado=False).all()
    result = []
    for m in mensajes:
        result.append({
            'Id': m.Id,
            'Mensaje': m.Mensaje,
            'FechaHora': m.FechaHora.strftime("%Y-%m-%d %H:%M"),
            'destinatario': m.destinatario.correo_electronico if m.destinatario else 'Desconocido'
        })
    return jsonify(result)

@app.route('/eliminados/<int:id_usuario>')
def eliminados(id_usuario):
    # Bandeja de eliminados
    mensajes = Comunicado.query.filter(
        ((Comunicado.IdUsuarioRemitente==id_usuario) | (Comunicado.IdUsuarioDestinatario==id_usuario)),
        Comunicado.Eliminado==True
    ).all()
    result = []
    for m in mensajes:
        result.append({
            'Id': m.Id,
            'Mensaje': m.Mensaje,
            'FechaHora': m.FechaHora.strftime("%Y-%m-%d %H:%M"),
            'nombre_rem': m.remitente.nombre_completo if m.remitente else 'Desconocido'
        })
    return jsonify(result)

@app.route('/enviar', methods=['POST'])
def enviar():
    # Enviar mensaje
    data = request.get_json()
    remitente_id = data['remitente_id']
    correo_destinatario = data['destinatario']
    mensaje = data['mensaje']

    destinatario = Usuario.query.filter_by(correo_electronico=correo_destinatario).first()
    if not destinatario:
        return jsonify({'error': 'El destinatario no existe'})

    nuevo = Comunicado(
        IdUsuarioRemitente=remitente_id,
        IdUsuarioDestinatario=destinatario.id,
        Mensaje=mensaje,
        FechaHora=datetime.now(),
        Eliminado=False
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({'mensaje': 'Correo enviado correctamente'})

@app.route('/correo/<int:id_correo>')
def ver_correo(id_correo):
    # Ver un correo en detalle
    correo = Comunicado.query.get(id_correo)
    return jsonify({
        'Id': correo.Id,
        'Mensaje': correo.Mensaje,
        'FechaHora': correo.FechaHora.strftime("%Y-%m-%d %H:%M"),
        'nombre_rem': correo.remitente.nombre_completo if correo.remitente else "Desconocido",
        'destinatario': correo.destinatario.correo_electronico if correo.destinatario else "Desconocido"
    })

@app.route('/eliminar/<int:id_correo>', methods=['POST'])
def eliminar(id_correo):
    # Eliminar (mover a eliminados)
    correo = Comunicado.query.get(id_correo)
    correo.Eliminado = True
    db.session.commit()
    return jsonify({'mensaje': 'Correo eliminado'})

@app.route('/recuperar/<int:id_correo>', methods=['POST'])
def recuperar(id_correo):
    # Recuperar de eliminados
    correo = Comunicado.query.get(id_correo)
    correo.Eliminado = False
    db.session.commit()
    return jsonify({'mensaje': 'Correo recuperado'})

@app.route("/eventos", methods=["GET"])
def obtener_eventos():
    eventos = Evento.query.all()
    return jsonify([e.to_dict() for e in eventos])

@app.route("/eventos/<rol>", methods=["GET"])
def obtener_eventos_por_rol(rol):
    eventos = Evento.query.filter_by(RolDestino=rol).all()
    return jsonify([e.to_dict() for e in eventos])

@app.route("/eventos", methods=["POST"])
def crear_evento():
    data = request.json
    try:
        nuevo_evento = Evento(
            Nombre=data["Nombre"],
            Descripcion=data["Descripcion"],
            Fecha=datetime.strptime(data["Fecha"], "%Y-%m-%d").date(),
            Hora=datetime.strptime(data["Hora"], "%H:%M").time(),
            RolDestino=data["RolDestino"]
        )
        db.session.add(nuevo_evento)
        db.session.commit()
        return jsonify({"mensaje": "Evento creado correctamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/eventos/<int:id>", methods=["DELETE"])
def eliminar_evento(id):
    evento = Evento.query.get(id)
    if not evento:
        return jsonify({"error": "Evento no encontrado"}), 404
    db.session.delete(evento)
    db.session.commit()
    return jsonify({"mensaje": "Evento eliminado correctamente"}), 200

# --- REGISTRO DE BLUEPRINTS ---
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(estudiante_bp)
app.register_blueprint(padre_bp)
app.register_blueprint(profesor_bp)

# --- MAIN ---
if __name__ == '__main__':
    with app.app_context():
        create_initial_data()
    app.run(debug=True) 
