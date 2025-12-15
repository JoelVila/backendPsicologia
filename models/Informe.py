# app/models/informe.py
from app.extensions import db
import datetime


class Informe(db.Model):
    __tablename__ = 'informe'

    id_informe = db.Column(db.Integer, primary_key=True)
    # FKs:
    id_paciente = db.Column(db.Integer)
    id_psicologo = db.Column(db.Integer)

    contenido = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    fecha_modificacion = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<Informe {self.id_informe}>'