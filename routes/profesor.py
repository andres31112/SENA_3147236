# routes/profesor.py
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from controllers.decorators import role_required
from app import db
from controllers.models import Profesor, Clase, AsignaturaHorario, Matricula, Estudiante, Email

profesor_bp = Blueprint('profesor', __name__, url_prefix='/profesor')

@profesor_bp.route('/dashboard')
@login_required
@role_required('profesor')
def dashboard():
    return render_template('profesores/dashboard.html')

@profesor_bp.route('/registrar_calificaciones')
@login_required
@role_required('profesor')
def registrar_calificaciones():
    profesor = db.session.query(Profesor).filter_by(usuarioId=current_user.id).first()
    clases = db.session.query(Clase).filter_by(profesorId=profesor.id).all() if profesor else []
    return render_template('profesores/registrar_calificaciones.html', clases=clases)

@profesor_bp.route('/ver_lista_estudiantes')
@login_required
@role_required('profesor')
def ver_lista_estudiantes():
    profesor = db.session.query(Profesor).filter_by(usuarioId=current_user.id).first()
    clases = db.session.query(Clase).filter_by(profesorId=profesor.id).all() if profesor else []
    estudiantes = []
    for clase in clases:
        matriculas = db.session.query(Matricula).filter_by(cursoId=clase.cursoId).all()
        estudiantes.extend([m.estudiante for m in matriculas])
    return render_template('profesores/ver_lista_estudiantes.html', estudiantes=estudiantes)

@profesor_bp.route('/ver_horario_clases')
@login_required
@role_required('profesor')
def ver_horario_clases():
    profesor = db.session.query(Profesor).filter_by(usuarioId=current_user.id).first()
    clases = db.session.query(Clase).filter_by(profesorId=profesor.id).all() if profesor else []
    horarios = [db.session.query(AsignaturaHorario).filter_by(asignaturaId=clase.asignaturaId).all() for clase in clases]
    return render_template('profesores/ver_horario_clases.html', horarios=horarios)

@profesor_bp.route('/comunicaciones')
@login_required
@role_required('profesor')
def comunicaciones():
    emails = db.session.query(Email).filter_by(destinatarioId=current_user.id).all()
    return render_template('profesores/comunicaciones.html', emails=emails)

@profesor_bp.route('/perfil')
@login_required
@role_required('profesor')
def perfil():
    return render_template('profesores/perfil.html')

@profesor_bp.route('/soporte')
@login_required
@role_required('profesor')
def soporte():
    return render_template('profesores/soporte.html')