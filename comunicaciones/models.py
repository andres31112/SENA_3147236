from app import db
from datetime import datetime

class Usuario(db.Model):
    __tablename__ = 'usuario'
    IdUsuario = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(100))
    Apellido = db.Column(db.String(100))
    Documento = db.Column(db.String(50))
    Correo = db.Column(db.String(100), unique=True)
    Contrasena = db.Column(db.String(100))
    Rol = db.Column(db.String(50))

class Comunicacion(db.Model):
    __tablename__ = 'comunicacion'
    Id = db.Column(db.Integer, primary_key=True)
    IdUsuarioRemitente = db.Column(db.Integer, db.ForeignKey('usuarios.IdUsuario'))
    IdUsuarioDestinatario = db.Column(db.Integer, db.ForeignKey('usuarios.IdUsuario'))
    Mensaje = db.Column(db.Text)
    FechaHora = db.Column(db.DateTime, default=datetime.now)
    Eliminado = db.Column(db.Boolean, default=False)
