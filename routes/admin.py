from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from controllers.decorators import role_required
from controllers.forms import RegistrationForm, UserEditForm
from extensions import db
from controllers.models import Usuario, Rol

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# ===============================
# Panel y vistas generales
# ===============================
@admin_bp.route('/dashboard')
@login_required
@role_required(1)
def admin_panel():
    return render_template('superadmin/gestion_usuarios/dashboard.html')


@admin_bp.route('/inicio')
@login_required
@role_required(1)
def inicio():
    return render_template('superadmin/inicio/inicio.html')


@admin_bp.route('/gestion_inventario')
@login_required
@role_required(1)
def gestion_i():
    return render_template('superadmin/gestion_inventario/gi.html')


@admin_bp.route('/equipos')
@login_required
@role_required(1)
def equipos():
    return render_template('superadmin/gestion_inventario/equipos.html')


@admin_bp.route('/salones')
@login_required
@role_required(1)
def salones():
    salones = db.session.query(Salon).all()
    return render_template('superadmin/gestion_inventario/salones.html', salones=salones)


@admin_bp.route('/gestion-salones')
@login_required
@role_required(1)
def gestion_salones():
    salones = db.session.query(Salon).all()
    total_salones = db.session.query(Salon).count()
    salas_computo = db.session.query(Salon).filter_by(tipo='sala_computo').count()
    salas_general = db.session.query(Salon).filter_by(tipo='sala_general').count()
    salas_especial = db.session.query(Salon).filter_by(tipo='sala_especial').count()
    return render_template(
        'superadmin/gestion_inventario/salones.html',
        total_salones=total_salones,
        salas_computo=salas_computo,
        salas_general=salas_general,
        salas_especial=salas_especial,
        salones=salones
    )


# ===============================
# Registro de salones y equipos
# ===============================
@admin_bp.route('/registro_salon', methods=['GET', 'POST'])
@login_required
@role_required(1)
def registro_salon():
    form = SalonForm()
    if form.validate_on_submit():
        nuevo_salon = Salon(
            nombre_salon=form.nombre_salon.data,
            tipo=form.tipo.data,
            sede=form.sede.data
        )
        db.session.add(nuevo_salon)
        db.session.commit()
        flash('Sala creada exitosamente ✅', 'success')
        return redirect(url_for('admin.salones'))
    return render_template('superadmin/gestion_inventario/registro_salon.html', title='Crear Nueva Sala', form=form)


@admin_bp.route('/registro_equipo', methods=['GET', 'POST'])
@login_required
@role_required(1)
def registro_equipo():
    return render_template('superadmin/gestion_inventario/registro_equipo.html')


@admin_bp.route('/registro_incidente', methods=['GET', 'POST'])
@login_required
@role_required('administrador')
def registro_incidente():
    return render_template('superadmin/gestion_inventario/registro_incidente.html')


# ===============================
# Profesores y estudiantes
# ===============================
@admin_bp.route('/profesores')
@login_required
@role_required(1)
def profesores():
    profesores = db.session.query(Profesor).all()
    return render_template('superadmin/gestion_usuarios/profesores.html', profesores=profesores)


@admin_bp.route('/api/profesores')
@login_required
@role_required(1)
def api_profesores():
    try:
        profesores = db.session.query(Profesor).all()
        lista_profesores = []
        for profesor in profesores:
            user = db.session.query(Usuario).get(profesor.usuarioId)
            if user:
                lista_profesores.append({
                    'id_usuario': user.id_usuario,
                    'no_identidad': user.no_identidad,
                    'nombre_completo': f"{user.nombre} {user.apellido}",
                    'correo': user.correo,
                    'telefono': getattr(user, 'telefono', ''),
                    'rol': user.rol.nombre if user.rol else '',
                    'estado': getattr(user, 'estado_cuenta', 'activa')
                })
        return jsonify({"data": lista_profesores})
    except Exception as e:
        print(f"Error en la API de profesores: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500


@admin_bp.route('/estudiantes')
@login_required
@role_required(1)
def estudiantes():
    estudiantes = db.session.query(Estudiante).all()
    return render_template('superadmin/gestion_usuarios/estudiantes.html', estudiantes=estudiantes)


# ===============================
# Crear usuario
# ===============================
@admin_bp.route('/crear_usuario', methods=['GET', 'POST'])
@login_required
@role_required(1)
def crear_usuario():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = Usuario(
            tipo_doc=form.tipo_doc.data,
            no_identidad=form.no_identidad.data,
            nombre=form.nombre.data,
            apellido=form.apellido.data,
            correo=form.correo.data,
            telefono=form.telefono.data,
            rol=form.rol.data,  # rol ya es un objeto Rol
            estado_cuenta='activa'  # si añadiste este campo
        )
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()

        flash(f'Usuario "{new_user.nombre} {new_user.apellido}" creado exitosamente!', 'success')
        return redirect(url_for('admin.profesores'))  # o la vista que corresponda

    return render_template(
        'superadmin/gestion_usuarios/crear_usuario.html',
        title='Crear Nuevo Usuario',
        form=form
    )


# ===============================
# Editar usuario
# ===============================
@admin_bp.route('/editar_usuario/<int:user_id>', methods=['GET', 'POST'])
@login_required
@role_required(1)
def editar_usuario(user_id):
    user = db.session.query(Usuario).get_or_404(user_id)
    form = UserEditForm(original_no_identidad=user.no_identidad, original_correo=user.correo)

    # Prellenar datos al cargar el formulario
    if request.method == 'GET':
        form.tipo_doc.data = user.tipo_doc
        form.no_identidad.data = user.no_identidad
        form.nombre.data = user.nombre
        form.apellido.data = user.apellido
        form.correo.data = user.correo
        form.telefono.data = getattr(user, 'telefono', '')
        form.estado_cuenta.data = getattr(user, 'estado_cuenta', 'activa')
        form.rol.data = user.rol

    if form.validate_on_submit():
        user.tipo_doc = form.tipo_doc.data
        user.no_identidad = form.no_identidad.data
        user.nombre = form.nombre.data
        user.apellido = form.apellido.data
        user.correo = form.correo.data
        user.telefono = form.telefono.data
        user.estado_cuenta = form.estado_cuenta.data
        user.rol = form.rol.data

        db.session.commit()
        flash(f'Usuario "{user.nombre_completo}" actualizado exitosamente!', 'success')
        return redirect(url_for('admin.profesores'))

    return render_template('superadmin/gestion_usuarios/editar_perfil.html',
                           title='Editar Usuario', form=form, user=user)


# ===============================
# Eliminar usuario
# ===============================
@admin_bp.route('/eliminar_usuario/<int:user_id>', methods=['POST'])
@login_required
@role_required(1)
def eliminar_usuario(user_id):
    user = db.session.query(Usuario).get_or_404(user_id)
    if user.id_usuario == current_user.id_usuario:
        flash('No puedes eliminar tu propia cuenta de administrador.', 'danger')
        return redirect(url_for('admin.profesores'))
    db.session.delete(user)
    db.session.commit()
    flash(f'Usuario "{user.nombre_completo}" eliminado exitosamente.', 'success')
    return redirect(url_for('admin.profesores'))
