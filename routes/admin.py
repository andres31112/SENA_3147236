from flask import *
from flask_login import *
from controllers.decorators import *
from controllers.forms import *
from controllers.models import *
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
@role_required('Super Admin')
def admin_panel():
    return render_template('superadmin/gestion_usuarios/dashboard.html')

@admin_bp.route('/inicio')
@login_required
def inicio():
    return render_template('superadmin/inicio/inicio.html')

# --- Rutas de Gestión de Inventario ---
@admin_bp.route('/gestion_inventario')
@login_required
@permission_required('gestion_inventario')
def gestion_i():
    return render_template('superadmin/gestion_inventario/gi.html')

@admin_bp.route('/equipos')
@login_required
@permission_required('gestion_inventario')
def equipos():
    return render_template('superadmin/gestion_inventario/equipos.html')

@admin_bp.route('/registro_equipo')
def registro_equipo():
    return render_template('superadmin/gestion_inventario/registro_equipo.html')

@admin_bp.route('/registro_incidente')
def registro_incidente():
    return render_template('superadmin/gestion_inventario/registro_incidente.html')


# --- Rutas de Gestión de Usuarios y Roles ---
@admin_bp.route('/profesores')
@login_required
@permission_required('gestion_usuarios')
def profesores():
    # Esta ruta ahora solo renderiza la plantilla HTML.
    return render_template('superadmin/gestion_usuarios/profesores.html')

@admin_bp.route('/api/profesores')
@login_required
@permission_required('gestion_usuarios')
def api_profesores():
    try:
        rol_profesor = Rol.query.filter_by(nombre_rol='Profesor').first()
        if not rol_profesor:
            return jsonify({"data": []}), 200

        profesores = Usuario.query.filter_by(id_rol_fk=rol_profesor.id_rol).all()
        
        lista_profesores = []
        for profesor in profesores:
            lista_profesores.append({
                'id_usuario': profesor.id_usuario,
                'numero_identidad': profesor.numero_identidad,
                'nombre_completo': profesor.nombre_completo,
                'correo_electronico': profesor.correo_electronico,
                'telefono_celular': profesor.telefono_celular,
                'rol': profesor.rol_obj.nombre_rol if profesor.rol_obj else 'N/A',
                'estado_cuenta': profesor.estado_cuenta
            })
        
        return jsonify({"data": lista_profesores})
    
    except Exception as e:
        print(f"Error en la API de profesores: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

@admin_bp.route('/estudiantes')
@login_required
@permission_required('gestion_usuarios')
def estudiantes():
    rol_estudiante = Rol.query.filter_by(nombre_rol='Estudiante').first()
    usuarios_estudiantes = Usuario.query.filter_by(id_rol_fk=rol_estudiante.id_rol).all() if rol_estudiante else []
    return render_template('superadmin/gestion_usuarios/estudiantes.html', usuarios=usuarios_estudiantes)

# ... (El resto de tus rutas de crear_rol, lista_rol, editar_rol, etc., siguen igual) ...

@admin_bp.route('/crear_rol', methods=['GET', 'POST'])
@login_required
@permission_required('crear_roles')
def crear_rol():
    form = RoleForm()
    if form.validate_on_submit():
        new_role = Rol(nombre_rol=form.nombre_rol.data, descripcion=form.descripcion.data)
        selected_permission_ids = form.permissions.data
        for perm_id in selected_permission_ids:
            permission = Permiso.query.get(perm_id)
            if permission:
                new_role.permisos.append(permission)
        db.session.add(new_role)
        db.session.commit()
        flash(f'Rol "{new_role.nombre_rol}" creado exitosamente y permisos asignados!', 'success')
        return redirect(url_for('admin.lista_rol'))
    return render_template('superadmin/gestion_usuarios/crear_rol.html', title='Crear Nuevo Rol', form=form)

@admin_bp.route('/lista_rol')
@login_required
@permission_required('ver_roles')
def lista_rol():
    roles = Rol.query.all()
    return render_template('superadmin/gestion_usuarios/lista_rol.html', title='Lista de Roles', roles=roles)

@admin_bp.route('/editar_rol/<int:role_id>', methods=['GET', 'POST'])
@login_required
@permission_required('editar_roles')
def editar_rol(role_id):
    role = Rol.query.get_or_404(role_id)
    form = RoleForm(original_nombre_rol=role.nombre_rol, obj=role)

    if form.validate_on_submit():
        role.nombre_rol = form.nombre_rol.data
        role.descripcion = form.descripcion.data
        role.permisos.clear()
        selected_permission_ids = form.permissions.data
        for perm_id in selected_permission_ids:
            permission = Permiso.query.get(perm_id)
            if permission:
                role.permisos.append(permission)
        db.session.commit()
        flash(f'Rol "{role.nombre_rol}" actualizado exitosamente!', 'success')
        return redirect(url_for('admin.lista_rol'))
    elif request.method == 'GET':
        form.permissions.data = [p.id_permiso for p in role.permisos]
    return render_template('superadmin/gestion_usuarios/editar_rol.html', title='Editar Rol', form=form, role=role)

@admin_bp.route('/eliminar_rol/<int:role_id>', methods=['POST'])
@login_required
@permission_required('eliminar_roles')
def eliminar_rol(role_id):
    role = Rol.query.get_or_404(role_id)
    if role.usuarios.count() > 0:
        flash(f'No se puede eliminar el rol "{role.nombre_rol}" porque tiene usuarios asociados. Desvincula los usuarios primero.', 'danger')
        return redirect(url_for('admin.lista_rol'))
    db.session.delete(role)
    db.session.commit()
    flash(f'Rol "{role.nombre_rol}" eliminado exitosamente!', 'success')
    return redirect(url_for('admin.lista_rol'))

@admin_bp.route('/crear_usuario', methods=['GET', 'POST'])
@login_required
@permission_required('gestion_usuarios')
def crear_usuario():
    form = RegistrationForm()
    if not current_user.has_role('Super Admin'):
        del form.rol

    if form.validate_on_submit():
        new_user = Usuario(
            numero_identidad=form.numero_identidad.data,
            tipo_documento=form.tipo_documento.data,
            nombre_completo=form.nombre_completo.data,
            correo_electronico=form.correo_electronico.data,
            telefono_celular=form.telefono_celular.data,
            estado_cuenta='activa'
        )
        new_user.set_password(form.password.data)
        
        if current_user.has_role('Super Admin'):
            if form.rol.data:
                new_user.rol_obj = form.rol.data
            else:
                flash("Por favor, selecciona un rol para el usuario.", 'danger')
                return render_template('superadmin/gestion_usuarios/crear_usuario.html', title='Crear Nuevo Usuario', form=form)
        else:
            default_role = Rol.query.filter_by(nombre_rol='Usuario Estándar').first()
            if default_role:
                new_user.rol_obj = default_role
            else:
                flash("Rol 'Usuario Estándar' no encontrado. Por favor, créalo o contacta a un administrador.", 'danger')
                return redirect(url_for('admin.crear_usuario'))

        db.session.add(new_user)
        db.session.commit()
        flash(f'Usuario "{new_user.nombre_completo}" creado exitosamente!', 'success')
        return redirect(url_for('admin.profesores'))

    return render_template('superadmin/gestion_usuarios/crear_usuario.html', title='Crear Nuevo Usuario', form=form)

@admin_bp.route('/editar_usuario/<int:user_id>', methods=['GET', 'POST'])
@login_required
@permission_required('gestion_usuarios')
def editar_usuario(user_id):
    user = Usuario.query.get_or_404(user_id)
    form = UserEditForm(
        original_numero_identidad=user.numero_identidad,
        original_correo_electronico=user.correo_electronico,
        obj=user
    )

    if not current_user.has_role('Super Admin'):
        del form.rol

    if form.validate_on_submit():
        user.numero_identidad = form.numero_identidad.data
        user.tipo_documento = form.tipo_documento.data
        user.nombre_completo = form.nombre_completo.data
        user.correo_electronico = form.correo_electronico.data
        user.telefono_celular = form.telefono_celular.data
        user.estado_cuenta = form.estado_cuenta.data

        if current_user.has_role('Super Admin'):
            if form.rol.data:
                user.rol_obj = form.rol.data
            else:
                flash("Por favor, selecciona un rol para el usuario.", 'danger')
                return render_template('superadmin/gestion_usuarios/editar_perfil.html', title='Editar Usuario', form=form, user=user)

        db.session.commit()
        flash(f'Usuario "{user.nombre_completo}" actualizado exitosamente!', 'success')
        return redirect(url_for('admin.profesores'))
    elif request.method == 'GET':
        if current_user.has_role('Super Admin') and user.rol_obj:
            form.rol.data = user.rol_obj

    return render_template('superadmin/gestion_usuarios/editar_perfil.html', title='Editar Usuario', form=form, user=user)

@admin_bp.route('/eliminar_usuario/<int:user_id>', methods=['POST'])
@login_required
@permission_required('gestion_usuarios')
def eliminar_usuario(user_id):
    user = Usuario.query.get_or_404(user_id)
    if user.id_usuario == current_user.id_usuario:
        flash('No puedes eliminar tu propia cuenta de Super Admin.', 'danger')
        return redirect(url_for('admin.profesores'))

    db.session.delete(user)
    db.session.commit()
    flash(f'Usuario "{user.nombre_completo}" eliminado exitosamente.', 'success')
    return redirect(url_for('admin.profesores'))





def registro():
    if request.method == 'POST':
        nombres = request.form.get('nombres')
        apellidos = request.form.get('apellidos')
        correo_personal = request.form.get('correoPersonal')
        contrasena = request.form.get('contrasena')
        num_doc = request.form.get('numDoc')
        telefono = request.form.get('telefono')
        direccion = request.form.get('direccion')
        rol = request.form.get('rol')

        if not all([nombres, apellidos, correo_personal, contrasena, num_doc, telefono, rol,direccion]):
            flash('Por favor, completa todos los campos requeridos.', 'danger')
            return render_template('registro.html')

        try:
            print(f"Usuario registrado: {nombres} {apellidos}, Rol: {rol}")
            
            flash('✅ Los datos se han guardado exitosamente.', 'success')
            
            return redirect(url_for('registro'))
            
        except Exception as e:
            print(f"Error al registrar usuario: {e}")
            flash('Ocurrió un error al guardar los datos. Inténtalo de nuevo.', 'danger')

    return render_template('registro.html')