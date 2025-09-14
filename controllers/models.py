# controllers/models.py
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db  


class Usuario(db.Model, UserMixin):
    __tablename__ = 'Usuario'
    id = db.Column(db.Integer, primary_key=True)
    tipoDoc = db.Column(db.String(20), nullable=False)
    noIdentidad = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    contraseña = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.Enum('activo', 'inactivo'), default='activo')
    rol = db.Column(db.Enum('estudiante', 'profesor', 'administrador', 'padre'), nullable=False)

    def get_id(self):
        return str(self.id)

    def set_password(self, password):
        self.contraseña = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.contraseña, password)

    def __repr__(self):
        return f"Usuario('{self.nombre} {self.apellido}', '{self.correo}')"

class Estudiante(db.Model):
    __tablename__ = 'Estudiante'
    id = db.Column(db.Integer, primary_key=True)
    usuarioId = db.Column(db.Integer, db.ForeignKey('Usuario.id'), unique=True, nullable=False)

class Profesor(db.Model):
    __tablename__ = 'Profesor'
    id = db.Column(db.Integer, primary_key=True)
    usuarioId = db.Column(db.Integer, db.ForeignKey('Usuario.id'), unique=True, nullable=False)

class Administrador(db.Model):
    __tablename__ = 'Administrador'
    id = db.Column(db.Integer, primary_key=True)
    usuarioId = db.Column(db.Integer, db.ForeignKey('Usuario.id'), unique=True, nullable=False)

class Padre(db.Model):
    __tablename__ = 'Padre'
    id = db.Column(db.Integer, primary_key=True)
    usuarioId = db.Column(db.Integer, db.ForeignKey('Usuario.id'), unique=True, nullable=False)
    noCelular = db.Column(db.String(20))

class PadreHijo(db.Model):
    __tablename__ = 'PadreHijo'
    id = db.Column(db.Integer, primary_key=True)
    padreId = db.Column(db.Integer, db.ForeignKey('Padre.id'), nullable=False)
    estudianteId = db.Column(db.Integer, db.ForeignKey('Estudiante.id'), nullable=False)

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
    estudianteId = db.Column(db.Integer, db.ForeignKey('Estudiante.id'), nullable=False)
    cursoId = db.Column(db.Integer, db.ForeignKey('Curso.id'), nullable=False)
    año = db.Column(db.Integer, nullable=False)

class Asignatura(db.Model):
    __tablename__ = 'Asignatura'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)

class Profesor_Asignatura(db.Model):
    __tablename__ = 'Profesor_Asignatura'
    id = db.Column(db.Integer, primary_key=True)
    profesorId = db.Column(db.Integer, db.ForeignKey('Profesor.id'), nullable=False)
    asignaturaId = db.Column(db.Integer, db.ForeignKey('Asignatura.id'), nullable=False)

class Clase(db.Model):
    __tablename__ = 'Clase'
    id = db.Column(db.Integer, primary_key=True)
    asignaturaId = db.Column(db.Integer, db.ForeignKey('Asignatura.id'), nullable=False)
    profesorId = db.Column(db.Integer, db.ForeignKey('Profesor.id'), nullable=False)
    cursoId = db.Column(db.Integer, db.ForeignKey('Curso.id'), nullable=False)
    horarioId = db.Column(db.Integer, db.ForeignKey('HorarioGeneral.id'), nullable=False)
    representanteCursoId = db.Column(db.Integer, db.ForeignKey('Estudiante.id'))

class HorarioGeneral(db.Model):
    __tablename__ = 'HorarioGeneral'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    horaInicio = db.Column(db.Time, nullable=False)
    horaFin = db.Column(db.Time, nullable=False)
    diasSemana = db.Column(db.String(100), nullable=False)  # Ej: 'Lunes,Martes,Miercoles'

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
    estudianteId = db.Column(db.Integer, db.ForeignKey('Estudiante.id'), nullable=False)
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
    estudianteId = db.Column(db.Integer, db.ForeignKey('Estudiante.id'), nullable=False)
    asignaturaId = db.Column(db.Integer, db.ForeignKey('Asignatura.id'), nullable=False)
    categoriaId = db.Column(db.Integer, db.ForeignKey('CategoriaCalificacion.id'), nullable=False)
    valor = db.Column(db.Numeric(5,2), nullable=False)
    observaciones = db.Column(db.Text)

class Email(db.Model):
    __tablename__ = 'Email'
    id = db.Column(db.Integer, primary_key=True)
    remitenteId = db.Column(db.Integer, db.ForeignKey('Usuario.id'), nullable=False)
    destinatarioId = db.Column(db.Integer, db.ForeignKey('Usuario.id'), nullable=False)
    asunto = db.Column(db.String(200), nullable=False)
    cuerpo = db.Column(db.Text, nullable=False)
    fechaEnvio = db.Column(db.DateTime, nullable=False)

class Evento(db.Model):
    __tablename__ = 'Evento'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    fecha = db.Column(db.Date, nullable=False)
    lugar = db.Column(db.String(200))
    creadorId = db.Column(db.Integer, db.ForeignKey('Usuario.id'), nullable=False)

class Periodo(db.Model):
    __tablename__ = 'Periodo'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    año = db.Column(db.Integer, nullable=False)
    fechaInicio = db.Column(db.Date, nullable=False)
    fechaFin = db.Column(db.Date, nullable=False)
    estado = db.Column(db.Enum('proximo', 'en_curso', 'finalizado'), nullable=False)

class JornadaElectoral(db.Model):
    __tablename__ = 'JornadaElectoral'
    id = db.Column(db.Integer, primary_key=True)
    periodoId = db.Column(db.Integer, db.ForeignKey('Periodo.id'), nullable=False)
    fechaInicio = db.Column(db.Date, nullable=False)
    fechaFin = db.Column(db.Date, nullable=False)

class Cargo(db.Model):
    __tablename__ = 'Cargo'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.Enum('personero', 'cabildante', 'contraloria'), nullable=False)
    descripcionCargo = db.Column(db.Text)

class Candidato(db.Model):
    __tablename__ = 'Candidato'
    id = db.Column(db.Integer, primary_key=True)
    jornadaElectoralId = db.Column(db.Integer, db.ForeignKey('JornadaElectoral.id'), nullable=False)
    estudianteId = db.Column(db.Integer, db.ForeignKey('Estudiante.id'), nullable=False)
    cargoId = db.Column(db.Integer, db.ForeignKey('Cargo.id'), nullable=False)
    foto = db.Column(db.LargeBinary)
    eslogan = db.Column(db.Text)
    propuestas = db.Column(db.Text)
    numeroTarjeton = db.Column(db.Integer, nullable=False)

class Voto(db.Model):
    __tablename__ = 'Voto'
    id = db.Column(db.Integer, primary_key=True)
    estudianteId = db.Column(db.Integer, db.ForeignKey('Estudiante.id'), nullable=False)
    candidatoId = db.Column(db.Integer, db.ForeignKey('Candidato.id'), nullable=False)
    jornadaElectoralId = db.Column(db.Integer, db.ForeignKey('JornadaElectoral.id'), nullable=False)
    fechaVoto = db.Column(db.Date, nullable=False)
    horaVoto = db.Column(db.Time, nullable=False)

class Salon(db.Model):
    __tablename__ = 'Salon'
    id = db.Column(db.Integer, primary_key=True)
    nombreSalon = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.Enum('sala_computo', 'sala_general', 'sala_especial'), nullable=False)
    sede = db.Column(db.String(100), nullable=False)

class Equipo(db.Model):
    __tablename__ = 'Equipo'
    id = db.Column(db.Integer, primary_key=True)
    salonId = db.Column(db.Integer, db.ForeignKey('Salon.id'), nullable=False)
    marca = db.Column(db.String(100))
    modelo = db.Column(db.String(100))
    descripcion = db.Column(db.Text)
    estadoActual = db.Column(db.String(50))

class RegistroIncidentes(db.Model):
    __tablename__ = 'RegistroIncidentes'
    id = db.Column(db.Integer, primary_key=True)
    salonId = db.Column(db.Integer, db.ForeignKey('Salon.id'))
    equipoId = db.Column(db.Integer, db.ForeignKey('Equipo.id'))
    usuarioId = db.Column(db.Integer, db.ForeignKey('Usuario.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    descripcionIncidente = db.Column(db.Text, nullable=False)