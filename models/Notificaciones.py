# app/models/notificaciones.py
from app.extensions import db


class Notificacion(db.Model):
    __tablename__ = 'notificaciones'

    id_notificacion = db.Column(db.Integer, primary_key=True)
    # FKs:
    id_paciente = db.Column(db.Integer)
    id_psicologo = db.Column(db.Integer)
    id_informe = db.Column(db.Integer)
    id_cita = db.Column(db.Integer)

    texto = db.Column(db.String(255))
    leida = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Notificacion {self.id_notificacion}>'