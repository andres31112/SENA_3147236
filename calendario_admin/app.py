from flask import Flask, render_template, request, jsonify
from config import Config
from models import db, Evento
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ping")
def ping():
    return jsonify({"mensaje": "Conectado a basedatos2 🚀"})

# Obtener todos los eventos (si lo necesitas aún)
@app.route("/eventos", methods=["GET"])
def obtener_eventos():
    eventos = Evento.query.all()
    return jsonify([e.to_dict() for e in eventos])

# ✅ Obtener eventos según rol
@app.route("/eventos/<rol>", methods=["GET"])
def obtener_eventos_por_rol(rol):
    eventos = Evento.query.filter_by(RolDestino=rol).all()
    return jsonify([e.to_dict() for e in eventos])

@app.route("/eventos", methods=["POST"])
def crear_evento():
    data = request.json
    try:
        nuevo_evento = Evento(
            Nombre=data["Nombre"],
            Descripcion=data["Descripcion"],
            Fecha=datetime.strptime(data["Fecha"], "%Y-%m-%d").date(),
            Hora=datetime.strptime(data["Hora"], "%H:%M").time(),
            RolDestino=data["RolDestino"]
        )
        db.session.add(nuevo_evento)
        db.session.commit()
        return jsonify({"mensaje": "Evento creado correctamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ✅ Eliminar evento
@app.route("/eventos/<int:id>", methods=["DELETE"])
def eliminar_evento(id):
    evento = Evento.query.get(id)
    if not evento:
        return jsonify({"error": "Evento no encontrado"}), 404
    db.session.delete(evento)
    db.session.commit()
    return jsonify({"mensaje": "Evento eliminado correctamente"}), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
