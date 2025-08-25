# decorators.py
from functools import wraps
from flask import flash, redirect, url_for, request
from flask_login import current_user

def role_required(role_name):
    """
    Decorador que verifica si el usuario actual tiene el rol especificado.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Por favor, inicia sesión para acceder a esta página.', 'info')
                return redirect(url_for('login', next=request.url))
            # Utiliza el método has_role actualizado del modelo Usuario
            if not current_user.has_role(role_name):
                flash(f'No tienes el rol necesario ({role_name}) para acceder a esta página.', 'danger')
                return redirect(url_for('gestion')) # Redirige a una página de inicio o acceso denegado
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def permission_required(permission_name):
    """
    Decorador que verifica si el usuario actual tiene el permiso especificado.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Por favor, inicia sesión para acceder a esta página.', 'info')
                return redirect(url_for('login', next=request.url))
            # Utiliza el método has_permission actualizado del modelo Usuario
            if not current_user.has_permission(permission_name):
                flash(f'No tienes el permiso necesario ({permission_name}) para acceder a esta página.', 'danger')
                return redirect(url_for('gestion')) # Redirige a una página de inicio o acceso denegado
            return f(*args, **kwargs)
        return decorated_function
    return decorator