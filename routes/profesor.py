from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required
from controllers.decorators import role_required, permission_required
from controllers.models import db, Asignatura, Calificacion

profesor_bp = Blueprint('profesor', __name__, url_prefix='/profesor')

@profesor_bp.route('/dashboard')
@login_required
@role_required('Profesor')
def dashboard():
    """Muestra el panel principal del profesor con resúmenes de sus clases y tareas."""
    return render_template('profesor/dashboard.html')

@profesor_bp.route('/registrar_calificaciones')
@login_required
@permission_required('registrar_calificaciones')
def registrar_calificaciones():
    """Permite al profesor registrar y editar calificaciones de sus estudiantes."""
    return render_template('profesor/registrar_calificaciones.html')

@profesor_bp.route('/ver_lista_estudiantes')
@login_required
@permission_required('ver_lista_estudiantes')
def ver_lista_estudiantes():
    """Muestra la lista de estudiantes de las asignaturas del profesor."""
    return render_template('profesor/ver_lista_estudiantes.html')

@profesor_bp.route('/ver_horario_clases')
@login_required
@permission_required('ver_horario_clases')
def ver_horario_clases():
    """Muestra el horario de clases del profesor."""
    return render_template('profesor/ver_horario_clases.html')

@profesor_bp.route('/comunicaciones')
@login_required
def comunicaciones():
    """Página para ver y enviar comunicaciones a estudiantes y padres."""
    return render_template('profesor/comunicaciones.html')

@profesor_bp.route('/perfil')
@login_required
def perfil():
    """Página para que el profesor gestione la información de su perfil."""
    return render_template('profesor/perfil.html')

@profesor_bp.route('/soporte')
@login_required
def soporte():
    """Página de soporte para el profesor."""
    return render_template('profesor/soporte.html')