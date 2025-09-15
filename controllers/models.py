from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from controllers.permisos import ROLE_PERMISSIONS

# ===============================h
# Roles
# ===============================
class Rol(db.Model):
    __tablename__ = 'roles'
    id_rol = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)

    # Relación inversa a usuarios
    usuarios = db.relationship('Usuario', back_populates='rol', lazy=True)


# ===============================
# Usuarios
# ===============================
class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True)
    tipo_doc = db.Column(db.String(20), nullable=False)
    no_identidad = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(200))
    password_hash = db.Column(db.Text, nullable=False)

    id_rol_fk = db.Column(db.Integer, db.ForeignKey('roles.id_rol'), nullable=False)
    rol = db.relationship('Rol', back_populates='usuarios', lazy='joined')
    estado_cuenta = db.Column(db.Enum('activa', 'inactiva', name='estado_cuenta_enum'), nullable=False, default='activa')
    # ------------------------------
    # Propiedad para nombre completo
    # ------------------------------
    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    # ------------------------------
    # Funciones de contraseña
    # ------------------------------
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # ------------------------------
    # Flask-Login: ID del usuario
    # ------------------------------
    def get_id(self):
        return str(self.id_usuario)

    # ------------------------------
    # Funciones de roles y permisos
    # ------------------------------
    def has_role(self, role_name):
        return self.rol.nombre.lower() == role_name.lower() if self.rol else False

    def has_permission(self, permiso_nombre):
        if not self.rol:
            return False
        return permiso_nombre in ROLE_PERMISSIONS.get(self.rol.nombre, [])


# ===============================
# Académico
# ===============================
class Sede(db.Model):
    __tablename__ = 'Sede'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)


class Curso(db.Model):
    __tablename__ = 'Curso'
    id = db.Column(db.Integer, primary_key=True)
    nombreCurso = db.Column(db.String(100), nullable=False)
    sedeId = db.Column(db.Integer, db.ForeignKey('Sede.id'), nullable=False)


class Matricula(db.Model):
    __tablename__ = 'Matricula'
    id = db.Column(db.Integer, primary_key=True)
    estudianteId = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    cursoId = db.Column(db.Integer, db.ForeignKey('Curso.id'), nullable=False)
    año = db.Column(db.Integer, nullable=False)


class Asignatura(db.Model):
    __tablename__ = 'Asignatura'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)


class Clase(db.Model):
    __tablename__ = 'Clase'
    id = db.Column(db.Integer, primary_key=True)
    asignaturaId = db.Column(db.Integer, db.ForeignKey('Asignatura.id'), nullable=False)
    profesorId = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    cursoId = db.Column(db.Integer, db.ForeignKey('Curso.id'), nullable=False)
    horarioId = db.Column(db.Integer, db.ForeignKey('HorarioGeneral.id'), nullable=False)
    representanteCursoId = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'))


class HorarioGeneral(db.Model):
    __tablename__ = 'HorarioGeneral'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    horaInicio = db.Column(db.Time, nullable=False)
    horaFin = db.Column(db.Time, nullable=False)
    diasSemana = db.Column(db.String(100), nullable=False)


class Descanso(db.Model):
    __tablename__ = 'Descanso'
    id = db.Column(db.Integer, primary_key=True)
    horarioId = db.Column(db.Integer, db.ForeignKey('HorarioGeneral.id'), nullable=False)
    horaInicio = db.Column(db.Time, nullable=False)
    horaFin = db.Column(db.Time, nullable=False)


class BloqueHorario(db.Model):
    __tablename__ = 'BloqueHorario'
    id = db.Column(db.Integer, primary_key=True)
    horaInicio = db.Column(db.Time, nullable=False)
    horaFin = db.Column(db.Time, nullable=False)


class AsignaturaHorario(db.Model):
    __tablename__ = 'AsignaturaHorario'
    id = db.Column(db.Integer, primary_key=True)
    asignaturaId = db.Column(db.Integer, db.ForeignKey('Asignatura.id'), nullable=False)
    horarioId = db.Column(db.Integer, db.ForeignKey('HorarioGeneral.id'), nullable=False)
    bloqueId = db.Column(db.Integer, db.ForeignKey('BloqueHorario.id'), nullable=False)


class Asistencia(db.Model):
    __tablename__ = 'Asistencia'
    id = db.Column(db.Integer, primary_key=True)
    estudianteId = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    claseId = db.Column(db.Integer, db.ForeignKey('Clase.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    estado = db.Column(db.Enum('presente', 'ausente', 'tarde', 'justificado'), nullable=False)


class ConfiguracionCalificacion(db.Model):
    __tablename__ = 'ConfiguracionCalificacion'
    id = db.Column(db.Integer, primary_key=True)
    notaMinima = db.Column(db.Numeric(5,2), nullable=False)
    notaMaxima = db.Column(db.Numeric(5,2), nullable=False)
    notaMinimaAprobacion = db.Column(db.Numeric(5,2), nullable=False)


class CategoriaCalificacion(db.Model):
    __tablename__ = 'CategoriaCalificacion'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(20), nullable=False)
    porcentaje = db.Column(db.Numeric(5,2), nullable=False)


class Calificacion(db.Model):
    __tablename__ = 'Calificacion'
    id = db.Column(db.Integer, primary_key=True)
    estudianteId = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    asignaturaId = db.Column(db.Integer, db.ForeignKey('Asignatura.id'), nullable=False)
    categoriaId = db.Column(db.Integer, db.ForeignKey('CategoriaCalificacion.id'), nullable=False)
    valor = db.Column(db.Numeric(5,2), nullable=False)
    observaciones = db.Column(db.Text)
