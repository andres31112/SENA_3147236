# proyecto_sena/routes/auth.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from controllers.models import Usuario
from controllers.forms import LoginForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.correo_electronico.data
        password = form.password.data

        user = Usuario.query.filter_by(correo_electronico=email).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Inicio de sesión exitoso.', 'success')
            
            # --- Lógica de redirección por rol ---
            if user.rol_obj.nombre_rol == 'Super Admin':
                return redirect(url_for('admin.admin_panel'))
            elif user.rol_obj.nombre_rol == 'Profesor':
                return redirect(url_for('profesor.dashboard'))
            elif user.rol_obj.nombre_rol == 'Estudiante':
                return redirect(url_for('estudiante.estudiante_panel'))
            elif user.rol_obj.nombre_rol == 'Padre':
                return redirect(url_for('padre.dashboard'))
            else:
                # Redirección por defecto para roles no especificados
                return redirect(url_for('main.index'))
        else:
            flash('Inicio de sesión fallido. Por favor, revisa tu correo electrónico y contraseña.', 'danger')
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('¡Has cerrado sesión!', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')