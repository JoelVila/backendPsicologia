# app/models/Administrador.py
from app.extensions import db

class Administrador(db.Model):
    __tablename__ = 'administrador'

    id_admin = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), default="Admin")
    correo_electronico = db.Column(db.String(120), unique=True, nullable=False, index=True)
    contrasenia = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f'<Administrador {self.correo_electronico}>'
