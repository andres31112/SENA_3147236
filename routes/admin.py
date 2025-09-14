# routes/admin.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from controllers.decorators import role_required
from controllers.forms import RegistrationForm, UserEditForm, SalonForm
from app import db
from controllers.models import Usuario, Estudiante, Profesor, Administrador, Padre, Salon

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
@role_required('administrador')
def admin_panel():
    return render_template('superadmin/gestion_usuarios/dashboard.html')

@admin_bp.route('/inicio')
@login_required
@role_required('administrador')
def inicio():
    return render_template('superadmin/inicio/inicio.html')

@admin_bp.route('/gestion_inventario')
@login_required
@role_required('administrador')
def gestion_i():
    return render_template('superadmin/gestion_inventario/gi.html')

@admin_bp.route('/equipos')
@login_required
@role_required('administrador')
def equipos():
    return render_template('superadmin/gestion_inventario/equipos.html')

@admin_bp.route('/salones')
@login_required
@role_required('administrador')
def salones():
    salones = db.session.query(Salon).all()
    return render_template('superadmin/gestion_inventario/salones.html', salones=salones)

@admin_bp.route('/gestion-salones')
@login_required
@role_required('administrador')
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

@admin_bp.route('/registro_salon', methods=['GET', 'POST'])
@login_required
@role_required('administrador')
def registro_salon():
    form = SalonForm()
    if form.validate_on_submit():
        nuevo_salon = Salon(
            nombreSalon=form.nombreSalon.data,
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
@role_required('administrador')
def registro_equipo():
    # Agrega lógica si es necesario, e.g., un formulario para Equipo
    return render_template('superadmin/gestion_inventario/registro_equipo.html')

@admin_bp.route('/registro_incidente', methods=['GET', 'POST'])
@login_required
@role_required('administrador')
def registro_incidente():
    # Agrega lógica si es necesario, e.g., un formulario para RegistroIncidentes
    return render_template('superadmin/gestion_inventario/registro_incidente.html')

@admin_bp.route('/profesores')
@login_required
@role_required('administrador')
def profesores():
    profesores = db.session.query(Profesor).all()
    return render_template('superadmin/gestion_usuarios/profesores.html', profesores=profesores)

@admin_bp.route('/api/profesores')
@login_required
@role_required('administrador')
def api_profesores():
    try:
        profesores = db.session.query(Profesor).all()
        lista_profesores = []
        for profesor in profesores:
            user = db.session.query(Usuario).get(profesor.usuarioId)
            if user:
                lista_profesores.append({
                    'id_usuario': user.id,
                    'noIdentidad': user.noIdentidad,
                    'nombre_completo': f"{user.nombre} {user.apellido}",
                    'correo': user.correo,
                    'noCelular': user.noCelular if hasattr(user, 'noCelular') else '',
                    'rol': user.rol,
                    'estado': user.estado
                })
        return jsonify({"data": lista_profesores})
    except Exception as e:
        print(f"Error en la API de profesores: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

@admin_bp.route('/estudiantes')
@login_required
@role_required('administrador')
def estudiantes():
    estudiantes = db.session.query(Estudiante).all()
    return render_template('superadmin/gestion_usuarios/estudiantes.html', estudiantes=estudiantes)

@admin_bp.route('/crear_usuario', methods=['GET', 'POST'])
@login_required
@role_required('administrador')
def crear_usuario():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = Usuario(
            tipoDoc=form.tipoDoc.data,
            noIdentidad=form.noIdentidad.data,
            nombre=form.nombre.data,
            apellido=form.apellido.data,
            correo=form.correo.data,
            estado='activo',
            rol=form.rol.data
        )
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        if form.rol.data == 'estudiante':
            estudiante = Estudiante(usuarioId=new_user.id)
            db.session.add(estudiante)
        elif form.rol.data == 'profesor':
            profesor = Profesor(usuarioId=new_user.id)
            db.session.add(profesor)
        elif form.rol.data == 'administrador':
            administrador = Administrador(usuarioId=new_user.id)
            db.session.add(administrador)
        elif form.rol.data == 'padre':
            padre = Padre(usuarioId=new_user.id, noCelular=form.noCelular.data)
            db.session.add(padre)
        db.session.commit()
        flash(f'Usuario "{new_user.nombre} {new_user.apellido}" creado exitosamente!', 'success')
        return redirect(url_for('admin.profesores'))
    return render_template('superadmin/gestion_usuarios/crear_usuario.html', title='Crear Nuevo Usuario', form=form)

@admin_bp.route('/editar_usuario/<int:user_id>', methods=['GET', 'POST'])
@login_required
@role_required('administrador')
def editar_usuario(user_id):
    user = db.session.query(Usuario).get_or_404(user_id)
    form = UserEditForm(original_noIdentidad=user.noIdentidad, original_correo=user.correo)
    if form.validate_on_submit():
        user.tipoDoc = form.tipoDoc.data
        user.noIdentidad = form.noIdentidad.data
        user.nombre = form.nombre.data
        user.apellido = form.apellido.data
        user.correo = form.correo.data
        user.estado = form.estado.data
        user.rol = form.rol.data
        db.session.commit()
        flash(f'Usuario "{user.nombre} {user.apellido}" actualizado exitosamente!', 'success')
        return redirect(url_for('admin.profesores'))
    return render_template('superadmin/gestion_usuarios/editar_perfil.html', title='Editar Usuario', form=form, user=user)

@admin_bp.route('/eliminar_usuario/<int:user_id>', methods=['POST'])
@login_required
@role_required('administrador')
def eliminar_usuario(user_id):
    user = db.session.query(Usuario).get_or_404(user_id)
    if user.id == current_user.id:
        flash('No puedes eliminar tu propia cuenta de administrador.', 'danger')
        return redirect(url_for('admin.profesores'))
    db.session.delete(user)
    db.session.commit()
    flash(f'Usuario "{user.nombre} {user.apellido}" eliminado exitosamente.', 'success')
    return redirect(url_for('admin.profesores'))