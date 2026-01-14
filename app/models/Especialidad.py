# app/models/especialidad.py
from app.extensions import db


class Especialidad(db.Model):
    __tablename__ = 'especialidad'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    
    # Relationship (one-to-many)
    psicologos = db.relationship('Psicologo', back_populates='especialidad', lazy=True)

    def __repr__(self):
        return f'<Especialidad {self.nombre}>'