# controllers/decorators.py
from functools import wraps
from flask import flash, redirect, url_for, request, abort
from flask_login import current_user
from controllers.permisos import ROLE_PERMISSIONS

def role_required(role_name_or_id):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Por favor, inicia sesión para acceder a esta página.', 'info')
                return redirect(url_for('auth.login', next=request.url))

            # Comparación directa por ID si se pasa un entero
            if isinstance(role_name_or_id, int):
                if current_user.id_rol_fk != role_name_or_id:
                    flash('No tienes el rol necesario para acceder a esta página.', 'danger')
                    return redirect(url_for('main.index'))
            else:
                # Comparación por nombre si se pasa un string
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
