from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from functools import wraps
from controllers.models import db, Usuario, Asignatura, Clase, Matricula, Calificacion
from controllers.permisos import ROLE_PERMISSIONS

profesor_bp = Blueprint('profesor', __name__, url_prefix='/profesor')


@profesor_bp.route('/dashboard')
@login_required
def dashboard():
    """Panel principal del profesor con resúmenes de sus clases y tareas"""
    # Traer todas las clases del profesor
    clases = Clase.query.filter_by(profesorId=current_user.id_usuario).all()
    return render_template('profesores/dashboard.html', clases=clases)


@profesor_bp.route('/registrar_calificaciones')
@login_required
def registrar_calificaciones():
    """Permite al profesor registrar y editar calificaciones de sus estudiantes"""
    # Traer todas las clases del profesor
    clases = Clase.query.filter_by(profesorId=current_user.id_usuario).all()

    # Traer calificaciones de los estudiantes de esas clases
    calificaciones = Calificacion.query.join(Clase, Calificacion.claseId==Clase.id)\
        .filter(Clase.profesorId==current_user.id_usuario).all()

    return render_template('profesor/registrar_calificaciones.html', calificaciones=calificaciones, clases=clases)


@profesor_bp.route('/ver_lista_estudiantes')
@login_required
def ver_lista_estudiantes():
    """Muestra la lista de estudiantes de las asignaturas del profesor"""
    # Traer todas las clases del profesor
    clases = Clase.query.filter_by(profesorId=current_user.id_usuario).all()
    estudiantes_por_clase = {}

    for clase in clases:
        estudiantes = Usuario.query.join(Matricula, Usuario.id_usuario==Matricula.estudianteId)\
            .filter(Matricula.cursoId==clase.cursoId, Usuario.rol.has(nombre='Estudiante')).all()
        estudiantes_por_clase[clase.id] = estudiantes

    return render_template('profesor/ver_lista_estudiantes.html', estudiantes_por_clase=estudiantes_por_clase, clases=clases)


@profesor_bp.route('/ver_horario_clases')
@login_required
def ver_horario_clases():
    """Muestra el horario de clases del profesor"""
    clases = Clase.query.filter_by(profesorId=current_user.id_usuario).all()
    return render_template('profesor/ver_horario_clases.html', clases=clases)


@profesor_bp.route('/comunicaciones')
@login_required
def comunicaciones():
    """Página para ver y enviar comunicaciones a estudiantes y padres"""
    return render_template('profesor/comunicaciones.html')

@profesor_bp.route('/asistencia')
@login_required
def asistencia():
    """Página para ver y enviar comunicaciones a estudiantes y padres"""
    return render_template('profesores/asistencia.html')

@profesor_bp.route('/cursos')
@login_required
def cursos():
    """Página para ver y enviar comunicaciones a estudiantes y padres"""
    return render_template('profesores/cursos.html')

@profesor_bp.route('/asignaturas')
@login_required
def asignaturas():
    """Página para ver y enviar comunicaciones a estudiantes y padres"""
    return render_template('profesores/asignaturas.html')



@profesor_bp.route('/perfil')
@login_required
def perfil():
    """Página para que el profesor gestione la información de su perfil"""
    return render_template('profesor/perfil.html')


@profesor_bp.route('/soporte')
@login_required
def soporte():
    """Página de soporte para el profesor"""
    return render_template('profesor/soporte.html')
