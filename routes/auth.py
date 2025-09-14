# routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app import db
from controllers.models import Usuario
from controllers.forms import LoginForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.correo.data
        password = form.password.data
        user = db.session.query(Usuario).filter_by(correo=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Inicio de sesión exitoso.', 'success')
            if user.rol == 'administrador':
                return redirect(url_for('admin.admin_panel'))
            elif user.rol == 'profesor':
                return redirect(url_for('profesor.dashboard'))
            elif user.rol == 'estudiante':
                return redirect(url_for('estudiante.estudiante_panel'))
            elif user.rol == 'padre':
                return redirect(url_for('padre.dashboard'))
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