# app/models/cita.py
from app.extensions import db


class Cita(db.Model):
    __tablename__ = 'cita'

    id_cita = db.Column(db.Integer, primary_key=True)
    id_alta = db.Column(db.Integer)
    fecha = db.Column(db.Date)
    hora = db.Column(db.Time)
    tipo_cita = db.Column(db.String(50))
    # FKs:
    id_psicologo = db.Column(db.Integer)
    id_paciente = db.Column(db.Integer)

    precio_cita = db.Column(db.Numeric(10, 2))

    def __repr__(self):
        return f'<Cita {self.id_cita} en {self.fecha}>'