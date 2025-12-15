# app/models/psicologo.py
from app.extensions import db


class Psicologo(db.Model):
    __tablename__ = 'psicologo'

    id_psicologo = db.Column(db.Integer, primary_key=True)
    correo_electronico = db.Column(db.String(120), unique=True, nullable=False, index=True)
    contrasenia = db.Column(db.String(256), nullable=False)  # Hash de contraseña
    informe_certificacion = db.Column(db.String(255))
    foto_psicologo = db.Column(db.String(255))
    tipo_especialidad = db.Column(db.String(100))
    cuenta_bancaria = db.Column(db.String(50))

    def __repr__(self):
        return f'<Psicologo {self.correo_electronico}>'