# controllers/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app import db
from controllers.models import Usuario

class RegistrationForm(FlaskForm):
    noIdentidad = StringField('Número de Identidad', validators=[DataRequired(), Length(min=5, max=20)])
    tipoDoc = SelectField('Tipo de Documento', choices=[
        ('cc', 'Cédula de Ciudadanía'),
        ('ti', 'Tarjeta de Identidad'),
        ('ce', 'Cédula de Extranjería'),
        ('ppt', 'Permiso por Protección Temporal'),
        ('pep', 'Permiso Especial de Permanencia'),
        ('registro_civil', 'Registro Civil')
    ], validators=[DataRequired()])
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=100)])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(min=2, max=100)])
    correo = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password')])
    noCelular = StringField('Teléfono Celular', validators=[Length(max=20)])
    rol = SelectField('Rol del Usuario', choices=[
        ('estudiante', 'Estudiante'),
        ('profesor', 'Profesor'),
        ('administrador', 'Administrador'),
        ('padre', 'Padre')
    ], validators=[DataRequired()])
    submit = SubmitField('Registrar Usuario')

    def validate_noIdentidad(self, noIdentidad):
        user = db.session.query(Usuario).filter_by(noIdentidad=noIdentidad.data).first()
        if user:
            raise ValidationError('Ese número de identidad ya está registrado.')

    def validate_correo(self, correo):
        user = db.session.query(Usuario).filter_by(correo=correo.data).first()
        if user:
            raise ValidationError('Ese correo electrónico ya está registrado.')

class LoginForm(FlaskForm):
    correo = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember = BooleanField('Recordarme')
    submit = SubmitField('Iniciar Sesión')

class UserEditForm(FlaskForm):
    noIdentidad = StringField('Número de Identidad', validators=[DataRequired(), Length(min=5, max=20)])
    tipoDoc = SelectField('Tipo de Documento', choices=[
        ('cc', 'Cédula de Ciudadanía'),
        ('ti', 'Tarjeta de Identidad'),
        ('ce', 'Cédula de Extranjería'),
        ('ppt', 'Permiso por Protección Temporal'),
        ('pep', 'Permiso Especial de Permanencia'),
        ('registro_civil', 'Registro Civil')
    ], validators=[DataRequired()])
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=100)])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(min=2, max=100)])
    correo = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    noCelular = StringField('Teléfono Celular', validators=[Length(max=20)])
    estado = SelectField('Estado de la Cuenta', choices=[
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo')
    ], validators=[DataRequired()])
    rol = SelectField('Rol del Usuario', choices=[
        ('estudiante', 'Estudiante'),
        ('profesor', 'Profesor'),
        ('administrador', 'Administrador'),
        ('padre', 'Padre')
    ], validators=[DataRequired()])
    submit = SubmitField('Actualizar Usuario')

    def __init__(self, original_noIdentidad, original_correo, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_noIdentidad = original_noIdentidad
        self.original_correo = original_correo

    def validate_noIdentidad(self, noIdentidad):
        if noIdentidad.data != self.original_noIdentidad:
            user = db.session.query(Usuario).filter_by(noIdentidad=noIdentidad.data).first()
            if user:
                raise ValidationError('Ese número de identidad ya está en uso.')

    def validate_correo(self, correo):
        if correo.data != self.original_correo:
            user = db.session.query(Usuario).filter_by(correo=correo.data).first()
            if user:
                raise ValidationError('Ese correo electrónico ya está registrado.')

class SalonForm(FlaskForm):
    sede = SelectField('Sede', choices=[], validators=[DataRequired()])
    nombreSalon = StringField('Nombre del Salón', validators=[DataRequired(), Length(max=100)])
    tipo = SelectField('Tipo de Salón', choices=[
        ('sala_computo', 'Sala de Cómputo'),
        ('sala_general', 'Sala General'),
        ('sala_especial', 'Sala Especial')
    ], validators=[DataRequired()])
    submit = SubmitField('Crear Sala')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sede.choices = [(s.id, s.nombre) for s in db.session.query(Sede).all()]