# app/models/paciente.py
from app.extensions import db


class Paciente(db.Model):
    __tablename__ = 'paciente'

    id_paciente = db.Column(db.Integer, primary_key=True)
    correo_electronico = db.Column(db.String(120), unique=True, nullable=False, index=True)
    contrasenia = db.Column(db.String(256), nullable=False)  # Hash de contraseña
    nombre_completo = db.Column(db.String(100))
    edad = db.Column(db.Integer)
    telefono = db.Column(db.String(20))
    foto_paciente = db.Column(db.String(255))
    tipo_tarjeta = db.Column(db.String(50))

    def __repr__(self):
        return f'<Paciente {self.nombre_completo}>'