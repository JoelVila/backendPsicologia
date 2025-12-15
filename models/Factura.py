# app/models/factura.py
from app.extensions import db
import datetime


class Factura(db.Model):
    __tablename__ = 'factura'

    id_factura = db.Column(db.Integer, primary_key=True)
    # FKs:
    id_paciente = db.Column(db.Integer)
    id_psicologo = db.Column(db.Integer)
    id_informe = db.Column(db.Integer)

    numero_factura = db.Column(db.String(50), unique=True, nullable=False)
    fecha_emision = db.Column(db.Date, default=datetime.date.today)

    def __repr__(self):
        return f'<Factura {self.numero_factura}>'