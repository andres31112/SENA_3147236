from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required
from controllers.decorators import role_required, permission_required
from controllers.models import db

padre_bp = Blueprint('padre', __name__, url_prefix='/padre')

@padre_bp.route('/dashboard')
@login_required
@role_required('Padre')
def dashboard():
    """Muestra el panel principal del padre con un resumen del progreso del hijo/a."""
    return render_template('padres/dashboard.html')

@padre_bp.route('/ver_calificaciones_hijo')
@login_required
@permission_required('ver_calificaciones_hijo')
def ver_calificaciones_hijo():
    """Permite al padre ver las calificaciones de su hijo/a."""
    return render_template('padre/ver_calificaciones_hijo.html')

@padre_bp.route('/ver_horario_hijo')
@login_required
@permission_required('ver_horario_hijo')
def ver_horario_hijo():
    """Muestra el horario de clases del hijo/a."""
    return render_template('padre/ver_horario_hijo.html')

@padre_bp.route('/comunicaciones')
@login_required
def comunicaciones():
    """Página para que el padre vea comunicados de la institución."""
    return render_template('padre/comunicaciones.html')

@padre_bp.route('/perfil')
@login_required
def perfil():
    """Página para que el padre gestione la información de su perfil."""
    return render_template('padre/perfil.html')

@padre_bp.route('/soporte')
@login_required
def soporte():
    """Página de soporte para el padre."""
    return render_template('padre/soporte.html')