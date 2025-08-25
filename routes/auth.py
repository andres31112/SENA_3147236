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
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin.admin_panel')) # Corregido para usar el nuevo blueprint
        else:
            flash('Inicio de sesión fallido. Por favor, revisa tu correo electrónico y contraseña.', 'danger')
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('¡Has cerrado sesión!', 'info')
    return redirect(url_for('main.index')) # Corregido para usar el nuevo blueprint

@auth_bp.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')