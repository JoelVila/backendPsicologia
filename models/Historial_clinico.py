# app/models/Historial_clinico.py
from app.extensions import db


class HistorialClinico(db.Model):
    __tablename__ = 'historial_clinico'

    id_historial = db.Column(db.Integer, primary_key=True)
    # FKs:
    id_paciente = db.Column(db.Integer)
    id_psicologo = db.Column(db.Integer)

    tipo_nota = db.Column(db.String(50))
    contenido = db.Column(db.Text)
    fecha = db.Column(db.Date)

    def __repr__(self):
        return f'<Historial {self.id_historial} de {self.id_paciente}>'