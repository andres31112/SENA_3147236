# routes/estudiantes.py
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from controllers.decorators import role_required, permission_required
from controllers.models import Usuario


# Se asume que tienes un nuevo Blueprint para las rutas de estudiante.
# Si no, puedes añadir esta ruta al Blueprint de 'admin' o crear uno nuevo llamado 'estudiante_bp'.
estudiante_bp = Blueprint('estudiante', __name__, url_prefix='/estudiante')

@estudiante_bp.route('/dashboard')
@login_required
def estudiante_panel():
    """
    Ruta para el dashboard del estudiante.
    Redirige a la página principal del panel de estudiante.
    """
    # Verifica si el usuario tiene rol 'Estudiante'
    if current_user.rol and current_user.rol.nombre.lower() == 'estudiante':
        return render_template('estudiantes/dashboard.html')
    else:
        flash('Acceso no autorizado.', 'danger')
        return redirect(url_for('auth.login')) 

    
# --- Ejemplo de ruta para ver calificaciones ---
@estudiante_bp.route('/calificaciones')
@login_required
@permission_required('ver_calificaciones')
def ver_calificaciones():
    """
    Ruta para que el estudiante vea sus calificaciones.
    """
    # Aquí iría la lógica para obtener las calificaciones del estudiante.
    # Por ejemplo: calificaciones = Calificacion.query.filter_by(id_estudiante=current_user.id).all()
    # return render_template('estudiante/calificaciones.html', calificaciones=calificaciones)
    return render_template('estudiante/calificaciones.html')

# --- Ejemplo de ruta para ver horario ---
@estudiante_bp.route('/horario')
@login_required
@permission_required('ver_horario')
def ver_horario():
    """
    Ruta para que el estudiante vea su horario.
    """
    # Aquí iría la lógica para obtener el horario del estudiante.
    # Por ejemplo: horario = Horario.query.filter_by(id_estudiante=current_user.id).all()
    # return render_template('estudiante/horario.html', horario=horario)
    return render_template('estudiante/horario.html')