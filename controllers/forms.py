# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, widgets, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField 
from controllers.models import * 

def get_all_roles():
    # Retorna todos los objetos Rol
    return Rol.query.order_by(Rol.nombre_rol).all()

def get_all_permissions():
    return Permiso.query.order_by(Permiso.descripcion).all()

class RegistrationForm(FlaskForm):
    numero_identidad = StringField('Número de Identidad', validators=[DataRequired(), Length(min=5, max=25)])
    tipo_documento = SelectField('Tipo de Documento', choices=[
        ('cc', 'Cédula de Ciudadanía'),
        ('ti', 'Tarjeta de Identidad'),
        ('ce', 'Cédula de Extranjería'),
        ('ppt', 'Permiso por Protección Temporal'),
        ('pep', 'Permiso Especial de Permanencia'),
        ('registro_civil', 'Registro Civil')
    ], validators=[DataRequired()])
    nombre_completo = StringField('Nombre Completo', validators=[DataRequired(), Length(min=2, max=100)])
    correo_electronico = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Contraseña',
                                     validators=[DataRequired(), EqualTo('password')])
    telefono_celular = StringField('Teléfono Celular', validators=[Length(max=20)])

    # Campo para seleccionar UN rol
    rol = QuerySelectField('Rol del Usuario', query_factory=get_all_roles,
                            get_pk=lambda a: a.id_rol,
                            get_label=lambda a: a.nombre_rol,
                            allow_blank=True, blank_text='Selecciona un Rol...')

    submit = SubmitField('Registrar Usuario')

    def validate_numero_identidad(self, numero_identidad):
        user = Usuario.query.filter_by(numero_identidad=numero_identidad.data).first()
        if user:
            raise ValidationError('Ese número de identidad ya está registrado. Por favor, elige uno diferente.')

    def validate_correo_electronico(self, correo_electronico):
        user = Usuario.query.filter_by(correo_electronico=correo_electronico.data).first()
        if user:
            raise ValidationError('Ese correo electrónico ya está registrado. Por favor, elige uno diferente.')

class LoginForm(FlaskForm):
    correo_electronico = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember = BooleanField('Recordarme')
    submit = SubmitField('Iniciar Sesión')

class RoleForm(FlaskForm):
    nombre_rol = StringField('Nombre del Rol', validators=[DataRequired(), Length(min=2, max=50)])
    descripcion = TextAreaField('Descripción del Rol', validators=[Length(max=255)])

    # Campo para asignar permisos al rol usando QuerySelectMultipleField
    permissions = QuerySelectMultipleField('Otorgar Permisos',
                                           query_factory=get_all_permissions,
                                           get_pk=lambda x: x.id_permiso,
                                           get_label=lambda x: x.descripcion, # Muestra la descripción del permiso
                                           widget=widgets.ListWidget(prefix_label=False),
                                           option_widget=widgets.CheckboxInput())
    submit = SubmitField('Guardar Rol')

    def __init__(self, original_nombre_rol=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_nombre_rol = original_nombre_rol

    def validate_nombre_rol(self, nombre_rol):
        if nombre_rol.data != self.original_nombre_rol:
            role = Rol.query.filter_by(nombre_rol=nombre_rol.data).first()
            if role:
                raise ValidationError('Este nombre de rol ya existe. Por favor, elige uno diferente.')

class UserEditForm(FlaskForm):
    numero_identidad = StringField('Número de Identidad', validators=[DataRequired(), Length(min=5, max=25)])
    tipo_documento = SelectField('Tipo de Documento', choices=[
        ('cc', 'Cédula de Ciudadanía'),
        ('ti', 'Tarjeta de Identidad'),
        ('ce', 'Cédula de Extranjería'),
        ('ppt', 'Permiso por Protección Temporal'),
        ('pep', 'Permiso Especial de Permanencia'),
        ('registro_civil', 'Registro Civil')
    ], validators=[DataRequired()])
    nombre_completo = StringField('Nombre Completo', validators=[DataRequired(), Length(min=2, max=100)])
    correo_electronico = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    telefono_celular = StringField('Teléfono Celular', validators=[Length(max=20)])
    estado_cuenta = SelectField('Estado de la Cuenta', choices=[
        ('activa', 'Activa'),
        ('inactiva', 'Inactiva')
    ], validators=[DataRequired()])

    # Campo para seleccionar UN rol
    rol = QuerySelectField('Rol del Usuario', query_factory=get_all_roles,
                            get_pk=lambda a: a.id_rol,
                            get_label=lambda a: a.nombre_rol,
                            allow_blank=True, blank_text='Selecciona un Rol...')

    submit = SubmitField('Actualizar Usuario')

    def __init__(self, original_numero_identidad, original_correo_electronico, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_numero_identidad = original_numero_identidad
        self.original_correo_electronico = original_correo_electronico

    def validate_numero_identidad(self, numero_identidad):
        if numero_identidad.data != self.original_numero_identidad:
            user = Usuario.query.filter_by(numero_identidad=numero_identidad.data).first()
            if user:
                raise ValidationError('Ese número de identidad ya está en uso. Por favor, elige uno diferente.')

    def validate_correo_electronico(self, correo_electronico):
        if correo_electronico.data != self.original_correo_electronico:
            user = Usuario.query.filter_by(correo_electronico=correo_electronico.data).first()
            if user:
                raise ValidationError('Ese correo electrónico ya está registrado. Por favor, elige uno diferente.')
            
from wtforms.validators import DataRequired, Length, NumberRange

class SalonForm(FlaskForm):
    id_sede_fk = SelectField(
        'Sede',
        choices=[(1, 'Sede A'), (2, 'Sede B')],
        coerce=int,
        validators=[DataRequired()]
    )

    nombre_salon = StringField(
        'Nombre del Salón',
        validators=[DataRequired(), Length(max=50)]
    )

    capacidad = IntegerField('Capacidad', validators=[DataRequired(), NumberRange(min=1)])
    tipo_salon = SelectField(
        'Tipo de Salón',
        choices=[
            ('aula', 'Aula'),
            ('laboratorio', 'Laboratorio'),
            ('auditorio', 'Auditorio'),
            ('sala_computo', 'Sala de Cómputo')
        ],
        validators=[DataRequired()]
    )
    cantidad_sillas = IntegerField(
        'Cantidad de Sillas',
        validators=[NumberRange(min=0)]
    )

    cantidad_mesas = IntegerField(
        'Cantidad de Mesas',
        validators=[NumberRange(min=0)]
    )

    submit = SubmitField('Crear Sala')
