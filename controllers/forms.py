from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms_sqlalchemy.fields import QuerySelectField
from controllers.models import Usuario, Rol

# ================================
# Funciones para QuerySelect
# ================================
def get_all_roles():
    """Retorna todos los roles ordenados por nombre."""
    return Rol.query.order_by(Rol.nombre).all()


# ================================
# Formulario de Registro
# ================================
class RegistrationForm(FlaskForm):
    no_identidad = StringField('Número de Identidad', validators=[DataRequired(), Length(min=5, max=25)])
    tipo_doc = SelectField('Tipo de Documento', choices=[
        ('cc', 'Cédula de Ciudadanía'),
        ('ti', 'Tarjeta de Identidad'),
        ('ce', 'Cédula de Extranjería'),
        ('ppt', 'Permiso por Protección Temporal'),
        ('pep', 'Permiso Especial de Permanencia'),
        ('registro_civil', 'Registro Civil')
    ], validators=[DataRequired()])
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=50)])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(min=2, max=50)])
    correo = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    telefono = StringField('Teléfono Celular', validators=[Length(max=20)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password')])
    rol = QuerySelectField('Rol del Usuario', query_factory=get_all_roles,
                           get_pk=lambda r: r.id_rol,
                           get_label=lambda r: r.nombre,
                           allow_blank=True, blank_text='Selecciona un Rol...')
    submit = SubmitField('Registrar Usuario')

    def validate_no_identidad(self, no_identidad):
        if Usuario.query.filter_by(no_identidad=no_identidad.data).first():
            raise ValidationError('Ese número de identidad ya está registrado. Por favor, elige uno diferente.')

    def validate_correo(self, correo):
        if Usuario.query.filter_by(correo=correo.data).first():
            raise ValidationError('Ese correo electrónico ya está registrado. Por favor, elige uno diferente.')


# ================================
# Formulario de Login
# ================================
class LoginForm(FlaskForm):
    correo = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember = BooleanField('Recordarme')
    submit = SubmitField('Iniciar Sesión')


# ================================
# Formulario de Roles
# ================================
class RoleForm(FlaskForm):
    nombre = StringField('Nombre del Rol', validators=[DataRequired(), Length(min=2, max=50)])
    descripcion = TextAreaField('Descripción del Rol', validators=[Length(max=255)])
    submit = SubmitField('Guardar Rol')

    def __init__(self, original_nombre=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_nombre = original_nombre

    def validate_nombre(self, nombre):
        if nombre.data != self.original_nombre:
            if Rol.query.filter_by(nombre=nombre.data).first():
                raise ValidationError('Este nombre de rol ya existe. Por favor, elige uno diferente.')


# ================================
# Formulario de Edición de Usuario
# ================================
class UserEditForm(FlaskForm):
    no_identidad = StringField('Número de Identidad', validators=[DataRequired(), Length(min=5, max=25)])
    tipo_doc = SelectField('Tipo de Documento', choices=[
        ('cc', 'Cédula de Ciudadanía'),
        ('ti', 'Tarjeta de Identidad'),
        ('ce', 'Cédula de Extranjería'),
        ('ppt', 'Permiso por Protección Temporal'),
        ('pep', 'Permiso Especial de Permanencia'),
        ('registro_civil', 'Registro Civil')
    ], validators=[DataRequired()])
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=50)])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(min=2, max=50)])
    correo = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    telefono = StringField('Teléfono Celular', validators=[Length(max=20)])
    estado_cuenta = SelectField('Estado de la Cuenta', choices=[
        ('activa', 'Activa'),
        ('inactiva', 'Inactiva')
    ], validators=[DataRequired()])
    rol = QuerySelectField('Rol del Usuario', query_factory=get_all_roles,
                           get_pk=lambda r: r.id_rol,
                           get_label=lambda r: r.nombre,
                           allow_blank=True, blank_text='Selecciona un Rol...')
    submit = SubmitField('Actualizar Usuario')

    def __init__(self, original_no_identidad=None, original_correo=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_no_identidad = original_no_identidad
        self.original_correo = original_correo

    def validate_no_identidad(self, no_identidad):
        if no_identidad.data != self.original_no_identidad:
            if Usuario.query.filter_by(no_identidad=no_identidad.data).first():
                raise ValidationError('Ese número de identidad ya está en uso. Por favor, elige uno diferente.')

    def validate_correo(self, correo):
        if correo.data != self.original_correo:
            if Usuario.query.filter_by(correo=correo.data).first():
                raise ValidationError('Ese correo electrónico ya está registrado. Por favor, elige uno diferente.')


# ================================
# Formulario de Solicitud de Restablecimiento de Contraseña
# ================================
class ForgotPasswordForm(FlaskForm):
    correo = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    submit = SubmitField('Solicitar Restablecimiento')


# ================================
# Formulario de Restablecimiento de Contraseña
# ================================
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Nueva Contraseña', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Restablecer Contraseña')