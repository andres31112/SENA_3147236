# controllers/decorators.py
from functools import wraps
from flask import flash, redirect, url_for, request, abort
from flask_login import current_user
from controllers.permisos import ROLE_PERMISSIONS

def role_required(role_name_or_id):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Asegúrate de que esta es la primera y única comprobación
            if not current_user.is_authenticated:
                flash('Por favor, inicia sesión para acceder a esta página.', 'info')
                return redirect(url_for('auth.login', next=request.url))

            # Ahora que sabes que el usuario está autenticado, puedes acceder a sus atributos
            if isinstance(role_name_or_id, int):
                # La lógica está bien, pero el problema es que el decorador se evalúa antes de la petición.
                # Para evitar esto, puedes asegurarte de que tu decorador no levanta errores
                # al ser evaluado en el momento de la carga de la app.
                if current_user.id_rol_fk != role_name_or_id:
                    flash('No tienes el rol necesario para acceder a esta página.', 'danger')
                    return redirect(url_for('main.index'))
            else:
                if not current_user.has_role(role_name_or_id):
                    flash('No tienes el rol necesario para acceder a esta página.', 'danger')
                    return redirect(url_for('main.index'))

            return f(*args, **kwargs)
        return decorated_function
    return decorator
def permission_required(permission_name):
    """
    Decorador que valida si el usuario tiene un permiso específico.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or not current_user.has_permission(permission_name):
                flash('No tienes permiso para acceder a esta página.', 'danger')
                return redirect(url_for('main.index'))  # Cambia al endpoint de inicio correcto
            return f(*args, **kwargs)
        return decorated_function
    return decorator
