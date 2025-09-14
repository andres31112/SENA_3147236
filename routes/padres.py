# routes/padres.py
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from controllers.decorators import role_required
from app import db
from controllers.models import Padre, PadreHijo, Calificacion, AsignaturaHorario, Clase, Matricula, Email

padre_bp = Blueprint('padre', __name__, url_prefix='/padre')

@padre_bp.route('/dashboard')
@login_required
@role_required('padre')
def dashboard():
    return render_template('padres/dashboard.html')

@padre_bp.route('/ver_calificaciones_hijo')
@login_required
@role_required('padre')
def ver_calificaciones_hijo():
    padre = db.session.query(Padre).filter_by(usuarioId=current_user.id).first()
    hijos = db.session.query(PadreHijo).filter_by(padreId=padre.id).all() if padre else []
    calificaciones = []
    for hijo in hijos:
        calificaciones.extend(db.session.query(Calificacion).filter_by(estudianteId=hijo.estudianteId).all())
    return render_template('padres/ver_calificaciones_hijo.html', calificaciones=calificaciones)

@padre_bp.route('/ver_horario_hijo')
@login_required
@role_required('padre')
def ver_horario_hijo():
    padre = db.session.query(Padre).filter_by(usuarioId=current_user.id).first()
    hijos = db.session.query(PadreHijo).filter_by(padreId=padre.id).all() if padre else []
    horarios = []
    for hijo in hijos:
        clases = db.session.query(Clase).join(Matricula).filter(Matricula.estudianteId == hijo.estudianteId).all()
        horarios.extend([db.session.query(AsignaturaHorario).filter_by(asignaturaId=clase.asignaturaId).all() for clase in clases])
    return render_template('padres/ver_horario_hijo.html', horarios=horarios)

@padre_bp.route('/comunicaciones')
@login_required
@role_required('padre')
def comunicaciones():
    emails = db.session.query(Email).filter_by(destinatarioId=current_user.id).all()
    return render_template('padres/comunicaciones.html', emails=emails)

@padre_bp.route('/perfil')
@login_required
@role_required('padre')
def perfil():
    return render_template('padres/perfil.html')

@padre_bp.route('/soporte')
@login_required
@role_required('padre')
def soporte():
    return render_template('padres/soporte.html')