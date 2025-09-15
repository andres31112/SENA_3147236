# proyecto_sena/routes/auth.py

#------------------------------------------------------------------#
#------------------------------------------------------------------#
#-----------no tocarrr---------------------------------------------#
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from controllers.models import Usuario
from controllers.forms import LoginForm
from extensions import db


auth_bp = Blueprint('auth', __name__)

ROL_REDIRECTS = {
    1: 'admin.admin_panel',        # Super Admin
    2: 'profesor.dashboard',      # Cambiar según función real
    3: 'estudiante.estudiante_panel',
    4: 'padre.dashboard'
}


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        correo = form.correo.data
        password = form.password.data

        # Buscar usuario por correo
        user = Usuario.query.filter_by(correo=correo).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Inicio de sesión exitoso.', 'success')
            print(f"Usuario: {user.nombre} {user.apellido}, Rol ID: {user.id_rol_fk}")


            # Redirección basada en id_rol
            ruta = ROL_REDIRECTS.get(user.id_rol_fk, 'main.index')
            return redirect(url_for(ruta))
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
