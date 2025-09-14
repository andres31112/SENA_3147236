# routes/estudiantes.py
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from controllers.decorators import role_required
from app import db
from controllers.models import Estudiante, Calificacion, AsignaturaHorario, Clase, Matricula

estudiantes_bp = Blueprint('estudiante', __name__, url_prefix='/estudiante')

@estudiantes_bp.route('/dashboard')
@login_required
@role_required('estudiante')
def estudiante_panel():
    return render_template('estudiantes/dashboard.html')

@estudiantes_bp.route('/calificaciones')
@login_required
@role_required('estudiante')
def ver_calificaciones():
    estudiante = db.session.query(Estudiante).filter_by(usuarioId=current_user.id).first()
    calificaciones = db.session.query(Calificacion).filter_by(estudianteId=estudiante.id).all() if estudiante else []
    return render_template('estudiantes/calificaciones.html', calificaciones=calificaciones)

@estudiantes_bp.route('/horario')
@login_required
@role_required('estudiante')
def ver_horario():
    estudiante = db.session.query(Estudiante).filter_by(usuarioId=current_user.id).first()
    clases = db.session.query(Clase).join(Matricula).filter(Matricula.estudianteId == estudiante.id).all() if estudiante else []
    horarios = [db.session.query(AsignaturaHorario).filter_by(asignaturaId=clase.asignaturaId).all() for clase in clases]
    return render_template('estudiantes/horario.html', horarios=horarios)