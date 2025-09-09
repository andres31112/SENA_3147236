from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Evento(db.Model):
    __tablename__ = "evento"

    IdEvento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nombre = db.Column(db.String(100), nullable=False)
    Descripcion = db.Column(db.Text)
    Fecha = db.Column(db.Date, nullable=False)
    Hora = db.Column(db.Time, nullable=False)
    RolDestino = db.Column(db.Enum( 'Profesor', 'Estudiante'), nullable=False)

    def to_dict(self):
        return {
            "IdEvento": self.IdEvento,
            "Nombre": self.Nombre,
            "Descripcion": self.Descripcion,
            "Fecha": self.Fecha.strftime("%Y-%m-%d"),
            "Hora": self.Hora.strftime("%H:%M"),
            "RolDestino": self.RolDestino
        }
