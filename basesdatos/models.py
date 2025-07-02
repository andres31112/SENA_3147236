from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

db = SQLAlchemy()

# Tabla de asociación para la relación muchos a muchos entre Usuarios y Roles.
usuario_roles = db.Table('usuario_roles',
    db.Column('id_usuario_fk', db.Integer, db.ForeignKey('usuarios.id_usuario'), primary_key=True),
    db.Column('id_rol_fk', db.Integer, db.ForeignKey('roles.id_rol'), primary_key=True)
)

# Tabla de asociación para la relación muchos a muchos entre Comunicaciones y Usuarios (destinatarios).
comunicacion_destinatarios = db.Table('comunicacion_destinatarios',
    db.Column('id_comunicacion_fk', db.Integer, db.ForeignKey('comunicaciones.id_comunicacion'), primary_key=True),
    db.Column('id_destinatario_fk', db.Integer, db.ForeignKey('usuarios.id_usuario'), primary_key=True),
    db.Column('leido', db.Boolean, default=False)
)


# --- MODELOS PRINCIPALES ---

class Usuario(db.Model, UserMixin):
    """
    Modelo para la tabla 'usuarios'.
    Centraliza la información de todos los tipos de usuarios (estudiantes, profesores, etc.).
    Hereda de UserMixin para ser compatible con Flask-Login.
    """
    __tablename__ = 'usuarios'
    
    id_usuario = db.Column(db.Integer, primary_key=True)
    numero_identidad = db.Column(db.String(25), unique=True, nullable=False)
    tipo_documento = db.Column(db.Enum('CC', 'TI', 'CE', 'PPT', 'PEP', 'Registro_Civil', name='tipo_documento_enum'), nullable=False)
    nombre_completo = db.Column(db.String(100), nullable=False)
    correo_electronico = db.Column(db.String(100), unique=True, nullable=False)
    contrasena_hash = db.Column(db.String(255), nullable=False)
    telefono_celular = db.Column(db.String(20), nullable=True)
    fecha_nacimiento = db.Column(db.Date, nullable=True)
    estado_cuenta = db.Column(db.Enum('Activa', 'Inactiva', name='estado_cuenta_enum'), nullable=False, default='Activa')

    # Relación Muchos a Muchos con Roles
    roles = db.relationship('Rol', secondary=usuario_roles, backref=db.backref('usuarios', lazy='dynamic'))

    # --- Métodos para Flask-Login ---
    def get_id(self):
        """Retorna el ID del usuario para Flask-Login."""
        return str(self.id_usuario)

    def set_password(self, password):
        """Genera y guarda el hash de la contraseña."""
        self.contrasena_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica si la contraseña proporcionada coincide con el hash almacenado."""
        return check_password_hash(self.contrasena_hash, password)

    def __repr__(self):
        return f"<Usuario {self.id_usuario}: {self.nombre_completo}>"

class Rol(db.Model):
    """ Modelo para la tabla de Roles. """
    __tablename__ = 'roles'
    id_rol = db.Column(db.Integer, primary_key=True)
    nombre_rol = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"<Rol {self.id_rol}: {self.nombre_rol}>"

class Sede(db.Model):
    """ Modelo para la tabla de Sedes de la institución. """
    __tablename__ = 'sedes'
    id_sede = db.Column(db.Integer, primary_key=True)
    nombre_sede = db.Column(db.String(100), unique=True, nullable=False)
    direccion = db.Column(db.String(255), nullable=False)

    # Relaciones Uno a Muchos
    cursos = db.relationship('Curso', backref='sede', lazy=True)
    salones = db.relationship('Salon', backref='sede', lazy=True)

    def __repr__(self):
        return f"<Sede {self.id_sede}: {self.nombre_sede}>"

class Curso(db.Model):
    """ Modelo para la tabla de Cursos/Grados. """
    __tablename__ = 'cursos'
    id_curso = db.Column(db.Integer, primary_key=True)
    id_sede_fk = db.Column(db.Integer, db.ForeignKey('sedes.id_sede'), nullable=False)
    nombre_curso = db.Column(db.String(50), nullable=False)
    id_director_curso_fk = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=True)
    id_representante_curso_fk = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=True)

    # Relaciones
    director = db.relationship('Usuario', foreign_keys=[id_director_curso_fk])
    representante = db.relationship('Usuario', foreign_keys=[id_representante_curso_fk])
    matriculas = db.relationship('Matricula', backref='curso', lazy=True)

    def __repr__(self):
        return f"<Curso {self.id_curso}: {self.nombre_curso}>"

class Asignatura(db.Model):
    """ Modelo para la tabla de Asignaturas. """
    __tablename__ = 'asignaturas'
    id_asignatura = db.Column(db.Integer, primary_key=True)
    nombre_asignatura = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<Asignatura {self.id_asignatura}: {self.nombre_asignatura}>"

class Salon(db.Model):
    """ Modelo para la tabla de Salones/Aulas. """
    __tablename__ = 'salones'
    id_salon = db.Column(db.Integer, primary_key=True)
    id_sede_fk = db.Column(db.Integer, db.ForeignKey('sedes.id_sede'), nullable=False)
    nombre_salon = db.Column(db.String(50), nullable=False)
    capacidad = db.Column(db.Integer, nullable=True)
    tipo_salon = db.Column(db.Enum('Aula', 'Laboratorio', 'Auditorio', 'Sala_Computo', name='tipo_salon_enum'), nullable=False, default='Aula')
    
    # Relaciones
    activos = db.relationship('Activo', backref='salon', lazy=True)

    def __repr__(self):
        return f"<Salon {self.id_salon}: {self.nombre_salon}>"

class Horario(db.Model):
    """ Modelo para la tabla de Horarios. """
    __tablename__ = 'horarios'
    id_horario = db.Column(db.Integer, primary_key=True)
    id_asignatura_fk = db.Column(db.Integer, db.ForeignKey('asignaturas.id_asignatura'), nullable=True)
    id_curso_fk = db.Column(db.Integer, db.ForeignKey('cursos.id_curso'), nullable=True)
    id_profesor_fk = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=True)
    id_salon_fk = db.Column(db.Integer, db.ForeignKey('salones.id_salon'), nullable=False)
    dia_semana = db.Column(db.Enum('Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo', name='dia_semana_enum'), nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)
    tipo_bloque = db.Column(db.Enum('Clase', 'Descanso', 'Evento', 'Reserva_Sala', name='tipo_bloque_enum'), nullable=False, default='Clase')
    descripcion_bloque = db.Column(db.String(255), nullable=True)

    # Relaciones
    asignatura = db.relationship('Asignatura', backref='horarios')
    curso = db.relationship('Curso', backref='horarios')
    profesor = db.relationship('Usuario', backref='horarios_impartidos')
    salon = db.relationship('Salon', backref='horarios')
    
    def __repr__(self):
        return f"<Horario {self.id_horario} en {self.salon.nombre_salon} el {self.dia_semana}>"

class Matricula(db.Model):
    """ Modelo para la tabla de Matrículas de estudiantes. """
    __tablename__ = 'matriculas'
    id_matricula = db.Column(db.Integer, primary_key=True)
    id_estudiante_fk = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    id_curso_fk = db.Column(db.Integer, db.ForeignKey('cursos.id_curso'), nullable=False)
    ano_academico = db.Column(db.Integer, nullable=False) # YEAR se puede manejar como Integer
    estado_matricula = db.Column(db.Enum('Activa', 'Retirado', 'Graduado', name='estado_matricula_enum'), nullable=False, default='Activa')

    # Relaciones
    estudiante = db.relationship('Usuario', backref='matriculas')
    
    def __repr__(self):
        return f"<Matricula {self.id_matricula} de {self.estudiante.nombre_completo} en {self.ano_academico}>"

class Asistencia(db.Model):
    """ Modelo para la tabla de Asistencia. """
    __tablename__ = 'asistencia'
    id_asistencia = db.Column(db.Integer, primary_key=True)
    id_matricula_fk = db.Column(db.Integer, db.ForeignKey('matriculas.id_matricula'), nullable=False)
    id_horario_fk = db.Column(db.Integer, db.ForeignKey('horarios.id_horario'), nullable=False)
    fecha_asistencia = db.Column(db.Date, nullable=False)
    estado_asistencia = db.Column(db.Enum('Presente', 'Ausente', 'Tardanza', 'Ausencia_Justificada', name='estado_asistencia_enum'), nullable=False)
    id_registrador_fk = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)

    # Relaciones
    matricula = db.relationship('Matricula', backref='asistencias')
    horario = db.relationship('Horario', backref='asistencias')
    registrador = db.relationship('Usuario', backref='asistencias_registradas')

    def __repr__(self):
        return f"<Asistencia {self.id_asistencia} para Matricula {self.id_matricula_fk} el {self.fecha_asistencia}>"

class Calificacion(db.Model):
    """ Modelo para la tabla de Calificaciones. """
    __tablename__ = 'calificaciones'
    id_calificacion = db.Column(db.Integer, primary_key=True)
    id_matricula_fk = db.Column(db.Integer, db.ForeignKey('matriculas.id_matricula'), nullable=False)
    id_asignatura_fk = db.Column(db.Integer, db.ForeignKey('asignaturas.id_asignatura'), nullable=False)
    periodo_academico = db.Column(db.String(50), nullable=False)
    nota_obtenida = db.Column(db.Numeric(5, 2), nullable=False)
    descripcion_evaluacion = db.Column(db.Text, nullable=True)
    id_profesor_fk = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)

    # Relaciones
    matricula = db.relationship('Matricula', backref='calificaciones')
    asignatura = db.relationship('Asignatura', backref='calificaciones')
    profesor = db.relationship('Usuario', backref='calificaciones_registradas')
    
    def __repr__(self):
        return f"<Calificacion {self.id_calificacion}: {self.nota_obtenida}>"

class Activo(db.Model):
    """ Modelo para la tabla de Activos (inventario). """
    __tablename__ = 'activos'
    id_activo = db.Column(db.Integer, primary_key=True)
    id_salon_fk = db.Column(db.Integer, db.ForeignKey('salones.id_salon'), nullable=True)
    tipo_activo = db.Column(db.Enum('Equipo_Computo', 'Mobiliario', 'Material_Educativo', 'Otro', name='tipo_activo_enum'), nullable=False)
    identificador_unico = db.Column(db.String(100), unique=True, nullable=False)
    nombre_activo = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(50), nullable=True)
    modelo = db.Column(db.String(50), nullable=True)
    descripcion = db.Column(db.Text, nullable=True)
    estado_activo = db.Column(db.Enum('Operativo', 'En Mantenimiento', 'Fuera_de_Servicio', 'Asignado', name='estado_activo_enum'), nullable=False, default='Operativo')

    def __repr__(self):
        return f"<Activo {self.id_activo}: {self.nombre_activo}>"

class IncidenteActivo(db.Model):
    """ Modelo para la tabla de Incidentes de Activos. """
    __tablename__ = 'incidentes_activos'
    id_incidente = db.Column(db.Integer, primary_key=True)
    id_activo_fk = db.Column(db.Integer, db.ForeignKey('activos.id_activo'), nullable=True)
    id_salon_fk = db.Column(db.Integer, db.ForeignKey('salones.id_salon'), nullable=True)
    id_usuario_reporta_fk = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    fecha_hora_incidente = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    descripcion_incidente = db.Column(db.Text, nullable=False)
    estado_incidente = db.Column(db.Enum('Abierto', 'En_Proceso', 'Resuelto', 'Cerrado_No_Resuelto', name='estado_incidente_enum'), nullable=False, default='Abierto')

    # Relaciones
    activo = db.relationship('Activo', backref='incidentes')
    salon = db.relationship('Salon', backref='incidentes')
    usuario_reporta = db.relationship('Usuario', backref='incidentes_reportados')

    def __repr__(self):
        return f"<Incidente {self.id_incidente} - {self.estado_incidente}>"

class MantenimientoActivo(db.Model):
    """ Modelo para la tabla de Mantenimientos de Activos. """
    __tablename__ = 'mantenimientos_activos'
    id_mantenimiento = db.Column(db.Integer, primary_key=True)
    id_activo_fk = db.Column(db.Integer, db.ForeignKey('activos.id_activo'), nullable=False)
    id_usuario_mantenimiento_fk = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    fecha_hora_mantenimiento = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    detalle_mantenimiento = db.Column(db.Text, nullable=False)
    estado_activo_posterior = db.Column(db.Enum('Operativo', 'En Mantenimiento', 'Fuera_de_Servicio', name='estado_activo_posterior_enum'), nullable=False)

    # Relaciones
    activo = db.relationship('Activo', backref='mantenimientos')
    tecnico = db.relationship('Usuario', backref='mantenimientos_realizados')

    def __repr__(self):
        return f"<Mantenimiento {self.id_mantenimiento} para Activo {self.id_activo_fk}>"

class Comunicacion(db.Model):
    """ Modelo para la tabla de Comunicaciones. """
    __tablename__ = 'comunicaciones'
    id_comunicacion = db.Column(db.Integer, primary_key=True)
    id_remitente_fk = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    asunto = db.Column(db.String(255), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    fecha_envio = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    # Relaciones
    remitente = db.relationship('Usuario', backref='comunicaciones_enviadas')
    destinatarios = db.relationship('Usuario', secondary=comunicacion_destinatarios, backref=db.backref('comunicaciones_recibidas', lazy='dynamic'))

    def __repr__(self):
        return f"<Comunicacion {self.id_comunicacion}: {self.asunto}>"

class Notificacion(db.Model):
    """ Modelo para la tabla de Notificaciones del sistema. """
    __tablename__ = 'notificaciones'
    id_notificacion = db.Column(db.Integer, primary_key=True)
    id_usuario_fk = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    tipo_notificacion = db.Column(db.String(50), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    leida = db.Column(db.Boolean, nullable=False, default=False)

    # Relaciones
    usuario = db.relationship('Usuario', backref='notificaciones')
    
    def __repr__(self):
        return f"<Notificacion {self.id_notificacion} para Usuario {self.id_usuario_fk}>"

class Evento(db.Model):
    """ Modelo para la tabla de Eventos del calendario. """
    __tablename__ = 'eventos'
    id_evento = db.Column(db.Integer, primary_key=True)
    id_creador_fk = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_fin = db.Column(db.DateTime, nullable=True)
    lugar = db.Column(db.String(255), nullable=True)
    tipo_evento = db.Column(db.Enum('Académico', 'Deportivo', 'Cultural', 'Administrativo', 'General', name='tipo_evento_enum'), nullable=False, default='General')

    # Relaciones
    creador = db.relationship('Usuario', backref='eventos_creados')

    def __repr__(self):
        return f"<Evento {self.id_evento}: {self.titulo}>"

class JornadaElectoral(db.Model):
    """ Modelo para la tabla de Jornadas Electorales. """
    __tablename__ = 'jornadas_electorales'
    id_jornada_electoral = db.Column(db.Integer, primary_key=True)
    nombre_jornada = db.Column(db.String(100), unique=True, nullable=False)
    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_fin = db.Column(db.DateTime, nullable=False)
    estado = db.Column(db.Enum('Activa', 'Inactiva', 'Finalizada', 'Cancelada', name='estado_jornada_enum'), nullable=False, default='Inactiva')
    id_organizador_fk = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=True)

    # Relaciones
    organizador = db.relationship('Usuario', backref='jornadas_organizadas')
    candidatos = db.relationship('Candidato', backref='jornada_electoral', lazy=True)
    votos = db.relationship('Voto', backref='jornada_electoral', lazy=True)

    def __repr__(self):
        return f"<JornadaElectoral {self.id_jornada_electoral}: {self.nombre_jornada}>"

class Candidato(db.Model):
    """ Modelo para la tabla de Candidatos para elecciones. """
    __tablename__ = 'candidatos'
    id_candidato = db.Column(db.Integer, primary_key=True)
    id_usuario_candidato_fk = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), unique=True, nullable=False)
    id_jornada_electoral_fk = db.Column(db.Integer, db.ForeignKey('jornadas_electorales.id_jornada_electoral'), nullable=False)
    cargo_postulado = db.Column(db.String(100), nullable=False)
    numero_tarjeton = db.Column(db.Integer, nullable=False)
    eslogan = db.Column(db.Text, nullable=True)
    propuestas = db.Column(db.Text, nullable=True)
    url_foto_perfil = db.Column(db.String(255), nullable=True)

    # Relaciones
    usuario = db.relationship('Usuario', backref='candidaturas')
    votos = db.relationship('Voto', backref='candidato', lazy=True)

    def __repr__(self):
        return f"<Candidato {self.id_candidato} para {self.cargo_postulado}>"

class Voto(db.Model):
    """ Modelo para la tabla de Votos. """
    __tablename__ = 'votos'
    id_voto = db.Column(db.Integer, primary_key=True)
    id_usuario_votante_fk = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    id_candidato_fk = db.Column(db.Integer, db.ForeignKey('candidatos.id_candidato'), nullable=False)
    id_jornada_electoral_fk = db.Column(db.Integer, db.ForeignKey('jornadas_electorales.id_jornada_electoral'), nullable=False)
    fecha_hora_voto = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    # Relaciones
    votante = db.relationship('Usuario', backref='votos_emitidos')

    def __repr__(self):
        return f"<Voto {self.id_voto} por Candidato {self.id_candidato_fk}>"
