from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# MODELOS
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

# RUTAS
@app.route('/')
def index():
    usuario = Usuario.query.get(1)  # Usuario logueado ejemplo
    return render_template('index.html', usuario=usuario)

@app.route('/mensajes/<int:id_usuario>')
def inbox(id_usuario):
    mensajes = Comunicacion.query.join(Usuario, Usuario.IdUsuario == Comunicacion.IdUsuarioRemitente)\
        .add_columns(Comunicacion.Id, Comunicacion.Mensaje, Comunicacion.FechaHora, Usuario.Nombre, Usuario.Apellido.label("Apellido"))\
        .filter(Comunicacion.IdUsuarioDestinatario==id_usuario, Comunicacion.Eliminado==False)\
        .all()
    result = []
    for m in mensajes:
        result.append({
            'Id': m.Id,
            'Mensaje': m.Mensaje,
            'FechaHora': m.FechaHora.strftime("%Y-%m-%d %H:%M"),
            'nombre_rem': f"{m.Nombre} {m.Apellido}"
        })
    return jsonify(result)

@app.route('/enviados/<int:id_usuario>')
def enviados(id_usuario):
    mensajes = Comunicacion.query.join(Usuario, Usuario.IdUsuario == Comunicacion.IdUsuarioDestinatario)\
        .add_columns(Comunicacion.Id, Comunicacion.Mensaje, Comunicacion.FechaHora, Usuario.Correo.label("destinatario"))\
        .filter(Comunicacion.IdUsuarioRemitente==id_usuario, Comunicacion.Eliminado==False)\
        .all()
    result = []
    for m in mensajes:
        result.append({
            'Id': m.Id,
            'Mensaje': m.Mensaje,
            'FechaHora': m.FechaHora.strftime("%Y-%m-%d %H:%M"),
            'destinatario': m.destinatario
        })
    return jsonify(result)

@app.route('/eliminados/<int:id_usuario>')
def eliminados(id_usuario):
    mensajes = Comunicacion.query.join(Usuario, Usuario.IdUsuario == Comunicacion.IdUsuarioRemitente)\
        .add_columns(Comunicacion.Id, Comunicacion.Mensaje, Comunicacion.FechaHora, Usuario.Nombre, Usuario.Apellido.label("Apellido"))\
        .filter(((Comunicacion.IdUsuarioRemitente==id_usuario) | (Comunicacion.IdUsuarioDestinatario==id_usuario)), Comunicacion.Eliminado==True)\
        .all()
    result = []
    for m in mensajes:
        result.append({
            'Id': m.Id,
            'Mensaje': m.Mensaje,
            'FechaHora': m.FechaHora.strftime("%Y-%m-%d %H:%M"),
            'nombre_rem': f"{m.Nombre} {m.Apellido}"
        })
    return jsonify(result)

@app.route('/enviar', methods=['POST'])
def enviar():
    data = request.get_json()
    remitente_id = data['remitente_id']
    correo_destinatario = data['destinatario']
    mensaje = data['mensaje']

    destinatario = Usuario.query.filter_by(Correo=correo_destinatario).first()
    if not destinatario:
        return jsonify({'error': 'El destinatario no existe'})

    nuevo = Comunicacion(
        IdUsuarioRemitente=remitente_id,
        IdUsuarioDestinatario=destinatario.IdUsuario,
        Mensaje=mensaje,
        FechaHora=datetime.now(),
        Eliminado=False
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({'mensaje': 'Correo enviado correctamente'})

@app.route('/correo/<int:id_correo>')
def ver_correo(id_correo):
    correo = Comunicacion.query.get(id_correo)
    remitente = Usuario.query.get(correo.IdUsuarioRemitente)
    destinatario = Usuario.query.get(correo.IdUsuarioDestinatario)
    return jsonify({
        'Id': correo.Id,
        'Mensaje': correo.Mensaje,
        'FechaHora': correo.FechaHora.strftime("%Y-%m-%d %H:%M"),
        'nombre_rem': f"{remitente.Nombre} {remitente.Apellido}",
        'destinatario': destinatario.Correo
    })

@app.route('/eliminar/<int:id_correo>', methods=['POST'])
def eliminar(id_correo):
    correo = Comunicacion.query.get(id_correo)
    correo.Eliminado = True
    db.session.commit()
    return jsonify({'mensaje': 'Correo eliminado'})

@app.route('/recuperar/<int:id_correo>', methods=['POST'])
def recuperar(id_correo):
    correo = Comunicacion.query.get(id_correo)
    correo.Eliminado = False
    db.session.commit()
    return jsonify({'mensaje': 'Correo recuperado'})

# MAIN
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Puerto alternativo
