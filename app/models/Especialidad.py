# app/models/especialidad.py
from app.extensions import db


# Association table for many-to-many relationship between Psicologo and Especialidad
psicologo_especialidad = db.Table('psicologo_especialidad',
    db.Column('psicologo_id', db.Integer, db.ForeignKey('psicologo.id_psicologo'), primary_key=True),
    db.Column('especialidad_id', db.Integer, db.ForeignKey('especialidad.id'), primary_key=True)
)


class Especialidad(db.Model):
    __tablename__ = 'especialidad'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    
    # Relationship (many-to-many)
    psicologos = db.relationship('Psicologo', secondary=psicologo_especialidad, back_populates='especialidades', lazy=True)

    def __repr__(self):
        return f'<Especialidad {self.nombre}>'