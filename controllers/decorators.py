# controllers/decorators.py
from functools import wraps
from flask import flash, redirect, url_for, request
from flask_login import current_user

def role_required(role_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Por favor, inicia sesión para acceder a esta página.', 'info')
                return redirect(url_for('auth.login', next=request.url))
            if current_user.rol != role_name:
                flash(f'No tienes el rol necesario ({role_name}) para acceder a esta página.', 'danger')
                return redirect(url_for('main.index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator