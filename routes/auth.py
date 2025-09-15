# proyecto_sena/routes/auth.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from controllers.models import Usuario
from extensions import db, mail
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
import os
from controllers.forms import LoginForm, ForgotPasswordForm, ResetPasswordForm

# --- Configuración del Serializador para tokens ---
# Se recomienda usar una variable de entorno para SECRET_KEY.
s = URLSafeTimedSerializer(os.getenv('SECRET_KEY', 'una-clave-super-secreta-cambiar'))

auth_bp = Blueprint('auth', __name__)

ROL_REDIRECTS = {
    1: 'admin.admin_panel',
    2: 'profesor.dashboard',
    3: 'estudiante.estudiante_panel',
    4: 'padre.dashboard'
}

# --- Rutas de Login y Logout (sin cambios) ---
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        correo = form.correo.data
        password = form.password.data
        user = Usuario.query.filter_by(correo=correo).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Inicio de sesión exitoso.', 'success')
            print(f"Usuario: {user.nombre} {user.apellido}, Rol ID: {user.id_rol_fk}")
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


## 3. Lógica para la Recuperación de Contraseña

# --- Función para enviar el correo de restablecimiento ---
def enviar_correo_restablecimiento(usuario):
    token = s.dumps(str(usuario.id_usuario), salt='recuperacion-password-salt')
    msg = Message('Restablecimiento de Contraseña',
                  sender=os.getenv('MAIL_USERNAME', 'noreply@tudominio.com'),
                  recipients=[usuario.correo])
    link = url_for('auth.restablecer_password', token=token, _external=True)
    msg.body = f'''
Hola {usuario.nombre_completo},

Recibimos una solicitud para restablecer tu contraseña. Haz clic en el siguiente enlace para continuar:
{link}

Si no solicitaste esto, ignora este correo.

Saludos,
Tu equipo.
'''
    mail.send(msg)


# --- Ruta para el formulario de "Olvidé mi contraseña" ---
@auth_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        correo = form.correo.data
        usuario = Usuario.query.filter_by(correo=correo).first()
        
        if usuario:
            enviar_correo_restablecimiento(usuario)
        
        # Mensaje genérico para evitar la enumeración de correos
        flash('Si la cuenta existe, se ha enviado un correo con las instrucciones para restablecer tu contraseña.', 'info')
        return redirect(url_for('auth.login'))
        
    return render_template('forgot_password.html', form=form)


# --- Ruta para el restablecimiento de contraseña con el token ---
@auth_bp.route('/restablecer_password/<token>', methods=['GET', 'POST'])
def restablecer_password(token):
    try:
        id_usuario = s.loads(token, salt='recuperacion-password-salt', max_age=3600)
    except:
        flash('El enlace de restablecimiento es inválido o ha expirado.', 'danger')
        return redirect(url_for('auth.forgot_password'))

    usuario = Usuario.query.get(id_usuario)
    if not usuario:
        flash('El usuario asociado al enlace no existe.', 'danger')
        return redirect(url_for('auth.forgot_password'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        nueva_password = form.password.data
        usuario.set_password(nueva_password)
        db.session.commit()
        flash('Tu contraseña ha sido restablecida con éxito. Ya puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))
            
    return render_template('restablecer_password.html', form=form)