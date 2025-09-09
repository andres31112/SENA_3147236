# basesdatos/models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# Tabla de asociación para la relación muchos a muchos entre Rol y Permiso
rol_permisos = db.Table('rol_permisos',
    db.Column('id_rol_fk', db.Integer, db.ForeignKey('roles.id_rol'), primary_key=True),
    db.Column('id_permiso_fk', db.Integer, db.ForeignKey('permisos.id_permiso'), primary_key=True)
)

# Tabla de asociación para la relación muchos a muchos entre Comunicado y Usuario (Destinatario)
destinatario_comunicado = db.Table('destinatario_comunicado',
    db.Column('id_comunicado_fk', db.Integer, db.ForeignKey('comunicados.id_comunicado'), primary_key=True),
    db.Column('id_destinatario_fk', db.Integer, db.ForeignKey('usuarios.id_usuario'), primary_key=True),
    db.Column('leido', db.Boolean, default=False)
)

class Permiso(db.Model):
    __tablename__ = 'permisos'
    id_permiso = db.Column(db.Integer, primary_key=True)
    nombre_permiso = db.Column(db.String(100), unique=True, nullable=False)
    descripcion = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Permiso '{self.nombre_permiso}'>"

class Rol(db.Model):
    __tablename__ = 'roles'
    id_rol = db.Column(db.Integer, primary_key=True)
    nombre_rol = db.Column(db.String(50), unique=True, nullable=False)
    descripcion = db.Column(db.Text, nullable=True)

    # Relación muchos a muchos con Permiso
    permisos = db.relationship('Permiso', secondary=rol_permisos, backref=db.backref('roles', lazy='dynamic'))
    # Relación uno a muchos con Usuario (un Rol tiene muchos Usuarios)
    usuarios = db.relationship('Usuario', back_populates='rol_obj') # Cambiado de 'rol' a 'rol_obj' para evitar conflicto con el atributo 'rol' de Usuario.

    def __repr__(self):
        return f"<Rol '{self.nombre_rol}'>"

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    
    id_usuario = db.Column(db.Integer, primary_key=True)
    numero_identidad = db.Column(db.String(25), unique=True, nullable=False)
    tipo_documento = db.Column(db.Enum('cc', 'ti', 'ce', 'ppt', 'pep', 'registro_civil', name='tipo_documento_enum'), nullable=False)
    nombre_completo = db.Column(db.String(100), nullable=False)
    correo_electronico = db.Column(db.String(100), unique=True, nullable=False)
    contrasena_hash = db.Column(db.String(255), nullable=False)
    telefono_celular = db.Column(db.String(20), nullable=True)
    fecha_nacimiento = db.Column(db.Date, nullable=True)
    estado_cuenta = db.Column(db.Enum('activa', 'inactiva', name='estado_cuenta_enum'), nullable=False, default='activa')
    id_rol_fk = db.Column(db.Integer, db.ForeignKey('roles.id_rol'), nullable=False)

    # Relación muchos a uno con Rol (un Usuario tiene un Rol)
    rol_obj = db.relationship('Rol', back_populates='usuarios') # Cambiado de 'rol' a 'rol_obj' para evitar conflicto con el atributo 'rol' de Usuario.

    def get_id(self):
        return str(self.id_usuario)

    def set_password(self, password):
        self.contrasena_hash = generate_password_hash(password)

    def check_password(self, password):
        # LÍNEA DE DEPURACIÓN AÑADIDA AQUÍ
        print(f"Comparando en models.py: Contraseña ingresada='{password}' con hash de DB='{self.contrasena_hash}'")
        return check_password_hash(self.contrasena_hash, password)
    
    # --- Método para verificar si el usuario tiene un ROL específico ---
    def has_role(self, role_name):
        return self.rol_obj and self.rol_obj.nombre_rol == role_name

    # --- Método para verificar si el usuario tiene un PERMISO específico ---
    def has_permission(self, permission_name):
        if not self.rol_obj:
            return False
        # Itera sobre los permisos del rol asignado al usuario
        for permission in self.rol_obj.permisos:
            if permission.nombre_permiso == permission_name:
                return True
        return False

    def __repr__(self):
        return f"Usuario('{self.nombre_completo}', '{self.correo_electronico}')"

# --- Resto de tus modelos, sin cambios si no se relacionan con Usuario, Rol o Permiso ---

class Sede(db.Model):
    __tablename__ = 'sedes'
    id_sede = db.Column(db.Integer, primary_key=True)
    nombre_sede = db.Column(db.String(100), unique=True, nullable=False)
    direccion = db.Column(db.String(255), nullable=False)

    salones = db.relationship("Salon", back_populates="sede")

class Curso(db.Model):
    __tablename__ = 'cursos'
    id_curso = db.Column(db.Integer, primary_key=True)
    id_sede_fk = db.Column(db.Integer, db.ForeignKey('sedes.id_sede'), nullable=False)
    nombre_curso = db.Column(db.String(50), nullable=False)
    id_director_curso_fk = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=True)
    id_representante_curso_fk = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=True)

class Asignatura(db.Model):
    __tablename__ = 'asignaturas'
    id_asignatura = db.Column(db.Integer, primary_key=True)
    nombre_asignatura = db.Column(db.String(100), unique=True, nullable=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
    activo_sn = db.Column(db.Enum('s', 'n', name='activo_sn_enum'), nullable=False, default='s')

class Salon(db.Model):
    __tablename__ = 'salones'
    id_salon = db.Column(db.Integer, primary_key=True)
    id_sede_fk = db.Column(db.Integer, db.ForeignKey("sedes.id_sede"), nullable=False)
    nombre_salon = db.Column(db.String(50), nullable=False)
    capacidad = db.Column(db.Integer, nullable=True)
    tipo_salon = db.Column(db.Enum('aula', 'laboratorio', 'auditorio', 'sala_computo', name='tipo_salon_enum'), nullable=False, default='aula')
    cantidad_sillas = db.Column(db.Integer, nullable=True)
    cantidad_mesas = db.Column(db.Integer, nullable=True)        
        
    sede = db.relationship("Sede", back_populates="salones")

class Periodo(db.Model):
    __tablename__ = 'periodos'
    id_periodo = db.Column(db.Integer, primary_key=True)
    nombre_periodo = db.Column(db.String(50), unique=True, nullable=False)
    año_periodo = db.Column(db.Integer, nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)
    estado_periodo = db.Column(db.Enum('activo', 'cerrado', 'proximo', name='estado_periodo_enum'), nullable=False, default='proximo')

class FranjaHoraria(db.Model):
    __tablename__ = 'franjas_horarias'
    id_franja_horaria = db.Column(db.Integer, primary_key=True)
    dia_semana = db.Column(db.Enum('lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo', name='dia_semana_enum'), nullable=False)
    hora_inicio_franja = db.Column(db.Time, nullable=False)
    hora_fin_franja = db.Column(db.Time, nullable=False)

class BloqueHorario(db.Model):
    __tablename__ = 'bloques_horarios'
    id_bloque_horario = db.Column(db.Integer, primary_key=True)
    id_franja_horaria_fk = db.Column(db.Integer, db.ForeignKey('franjas_horarias.id_franja_horaria'), nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)
    tipo_bloque = db.Column(db.Enum('descanso', 'clase', name='tipo_bloque_enum'), nullable=False)

class Horario(db.Model):
    __tablename__ = 'horarios'
    id_horario = db.Column(db.Integer, primary_key=True)
    id_periodo_fk = db.Column(db.Integer, db.ForeignKey('periodos.id_periodo'), nullable=False)
    id_franja_horaria_fk = db.Column(db.Integer, db.ForeignKey('franjas_horarias.id_franja_horaria'), nullable=False)
    id_bloque_horario_fk = db.Column(db.Integer, db.ForeignKey('bloques_horarios.id_bloque_horario'), nullable=False)
    id_asignatura_fk = db.Column(db.Integer, db.ForeignKey('asignaturas.id_asignatura'), nullable=True)
    id_curso_fk = db.Column(db.Integer, db.ForeignKey('cursos.id_curso'), nullable=True)
    id_profesor_fk = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=True)
    id_salon_fk = db.Column(db.Integer, db.ForeignKey('salones.id_salon'), nullable=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
    activo_sn = db.Column(db.Enum('s', 'n', name='horarios_activo_sn_enum'), nullable=False, default='s')

class Matricula(db.Model):
    __tablename__ = 'matriculas'
    id_matricula = db.Column(db.Integer, primary_key=True)
    id_estudiante_fk = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    id_curso_fk = db.Column(db.Integer, db.ForeignKey('cursos.id_curso'), nullable=False)
    año_academico = db.Column(db.Integer, nullable=False)
    estado_matricula = db.Column(db.Enum('activo', 'retirado', 'graduado', name='estado_matricula_enum'), nullable=False, default='activo')

class Asistencia(db.Model):
    __tablename__ = 'asistencia'
    id_asistencia = db.Column(db.Integer, primary_key=True)
    id_matricula_fk = db.Column(db.Integer, db.ForeignKey('matriculas.id_matricula'), nullable=False)
    id_horario_fk = db.Column(db.Integer, db.ForeignKey('horarios.id_horario'), nullable=False)
    fecha_asistencia = db.Column(db.Date, nullable=False)
    estado_asistencia = db.Column(db.Enum('presente', 'ausente', 'tardanza', 'justificada', name='estado_asistencia_enum'), nullable=False)
    id_registrador_fk = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    activo_sn = db.Column(db.Enum('s', 'n', name='asistencia_activo_sn_enum'), nullable=False, default='s')

class TipoCalificacion(db.Model):
    __tablename__ = 'tipo_calificacion'
    id_tipo_calificacion = db.Column(db.Integer, primary_key=True)
    nombre_tipo = db.Column(db.String(50), unique=True, nullable=False)
    porcentaje_asignado = db.Column(db.Numeric(5, 2), nullable=True)

class ActividadEvaluada(db.Model):
    __tablename__ = 'actividades_evaluadas'
    id_actividad_evaluada = db.Column(db.Integer, primary_key=True)
    id_asignatura_fk = db.Column(db.Integer, db.ForeignKey('asignaturas.id_asignatura'), nullable=False)
    id_tipo_calificacion_fk = db.Column(db.Integer, db.ForeignKey('tipo_calificacion.id_tipo_calificacion'), nullable=True)
    nombre_actividad = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)

class Calificacion(db.Model):
    __tablename__ = 'calificaciones'
    id_calificacion = db.Column(db.Integer, primary_key=True)
    id_actividad_evaluada_fk = db.Column(db.Integer, db.ForeignKey('actividades_evaluadas.id_actividad_evaluada'), nullable=False)
    id_matricula_fk = db.Column(db.Integer, db.ForeignKey('matriculas.id_matricula'), nullable=False)
    nota_obtenida = db.Column(db.Numeric(5, 2), nullable=False)
    observaciones = db.Column(db.Text, nullable=True)
    id_profesor_fk = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)

class Activo(db.Model):
    __tablename__ = 'activos'
    id_activo = db.Column(db.Integer, primary_key=True)
    id_salon_fk = db.Column(db.Integer, db.ForeignKey('salones.id_salon'), nullable=True)
    tipo_activo = db.Column(db.Enum('equipo_computo','mobiliario','material_educativo','otro', name='tipo_activo_enum'), nullable=False)
    identificador_unico = db.Column(db.String(100), unique=True, nullable=False)
    nombre_activo = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(50), nullable=True)
    modelo = db.Column(db.String(50), nullable=True)
    descripcion = db.Column(db.Text, nullable=True)
    estado_activo = db.Column(db.Enum('operativo', 'en_mantenimiento', 'fuera_de_servicio', 'asignado', name='estado_activo_enum'), nullable=False, default='operativo')

class RegistroIncidente(db.Model):
    __tablename__ = 'registro_incidentes'
    id_incidente = db.Column(db.Integer, primary_key=True)
    id_equipo_fk = db.Column(db.Integer, db.ForeignKey('activos.id_activo'), nullable=True)
    id_sala_computo_fk = db.Column(db.Integer, db.ForeignKey('salones.id_salon'), nullable=False)
    id_usuario_reporta_fk = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    fecha_incidente = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
    descripcion_incidente = db.Column(db.Text, nullable=False)

class AsignacionEquipo(db.Model):
    __tablename__ = 'asignacion_equipos'
    id_asignacion = db.Column(db.Integer, primary_key=True)
    id_equipo_fk = db.Column(db.Integer, db.ForeignKey('activos.id_activo'), nullable=False)
    id_usuario_asignado_fk = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    id_usuario_asignador_fk = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    fecha_asignacion = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
    estado_asignacion = db.Column(db.Enum('asignado','devuelto','en_uso','cancelado', name='estado_asignacion_enum'), nullable=False, default='asignado')

class RegistroMantenimiento(db.Model):
    __tablename__ = 'registro_mantenimiento'
    id_registro_mantenimiento = db.Column(db.Integer, primary_key=True)
    id_equipo_fk = db.Column(db.Integer, db.ForeignKey('activos.id_activo'), nullable=False)
    id_usuario_mantenimiento_fk = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    fecha_mantenimiento = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
    detalle_mantenimiento = db.Column(db.Text, nullable=False)
    estado_final_equipo = db.Column(db.Text, nullable=False)

class Comunicado(db.Model):
    __tablename__ = 'comunicados'
    id_comunicado = db.Column(db.Integer, primary_key=True)
    id_remitente_fk = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    asunto = db.Column(db.String(255), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    fecha_envio = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
    id_comunicado_inicial_fk = db.Column(db.Integer, db.ForeignKey('comunicados.id_comunicado'), nullable=True)
    destinatarios = db.relationship('Usuario', secondary=destinatario_comunicado, backref='comunicaciones_recibidas')

class Reaccion(db.Model):
    __tablename__ = 'reaccion'
    id_reaccion = db.Column(db.Integer, primary_key=True)
    id_comunicado_fk = db.Column(db.Integer, db.ForeignKey('comunicados.id_comunicado'), nullable=False)
    id_usuario_reacciona_fk = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    tipo_reaccion = db.Column(db.String(50), nullable=False)
    fecha_hora_reaccion = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())

class Evento(db.Model):
    __tablename__ = 'eventos'
    id_evento = db.Column(db.Integer, primary_key=True)
    id_creador_fk = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_fin = db.Column(db.DateTime, nullable=True)
    lugar = db.Column(db.String(255), nullable=True)

class Notificacion(db.Model):
    __tablename__ = 'notificaciones'
    id_notificacion = db.Column(db.Integer, primary_key=True)
    id_usuario_fk = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    tipo_notificacion = db.Column(db.String(50), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
    leida = db.Column(db.Boolean, nullable=False, default=False)

class JornadaElectoral(db.Model):
    __tablename__ = 'jornadas_electorales'
    id_jornada_electoral = db.Column(db.Integer, primary_key=True)
    nombre_jornada = db.Column(db.String(100), unique=True, nullable=False)
    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_fin = db.Column(db.DateTime, nullable=False)
    estado = db.Column(db.Enum('activa','inactiva','finalizada','cancelada', name='estado_jornada_enum'), nullable=False, default='inactiva')
    id_organizador_fk = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=True)

class Cargo(db.Model):
    __tablename__ = 'cargos'
    id_cargo = db.Column(db.Integer, primary_key=True)
    nombre_cargo = db.Column(db.String(100), unique=True, nullable=False)

class Candidato(db.Model):
    __tablename__ = 'candidatos'
    id_candidato = db.Column(db.Integer, primary_key=True)
    id_usuario_candidato_fk = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), unique=True, nullable=False)
    id_jornada_electoral_fk = db.Column(db.Integer, db.ForeignKey('jornadas_electorales.id_jornada_electoral'), nullable=False)
    id_cargo_fk = db.Column(db.Integer, db.ForeignKey('cargos.id_cargo'), nullable=False)
    numero_tarjeton = db.Column(db.Integer, nullable=False)
    eslogan = db.Column(db.Text, nullable=True)
    propuestas = db.Column(db.Text, nullable=True)
    url_foto_perfil = db.Column(db.String(255), nullable=True)

class Voto(db.Model):
    __tablename__ = 'votos'
    id_voto = db.Column(db.Integer, primary_key=True)
    id_usuario_votante_fk = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    id_candidato_fk = db.Column(db.Integer, db.ForeignKey('candidatos.id_candidato'), nullable=False)
    id_jornada_electoral_fk = db.Column(db.Integer, db.ForeignKey('jornadas_electorales.id_jornada_electoral'), nullable=False)
    id_cargo_fk = db.Column(db.Integer, db.ForeignKey('cargos.id_cargo'), nullable=False)
    fecha_hora_voto = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())