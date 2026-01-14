# app/models/psicologo.py
from app.extensions import db
# app/models/psicologo.py
from app.extensions import db


class Psicologo(db.Model):
    __tablename__ = 'psicologo'

    id_psicologo = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    correo_electronico = db.Column(db.String(120), unique=True, nullable=False, index=True)
    contrasenia = db.Column(db.String(256), nullable=False)  # Hash de contraseña
    telefono = db.Column(db.String(20))
    foto_psicologo = db.Column(db.String(255))
    bio = db.Column(db.Text)
    verificado = db.Column(db.Boolean, default=False)
    anios_experiencia = db.Column(db.Integer)
    
    # Precios
    precio_presencial = db.Column(db.Float)
    precio_online = db.Column(db.Float)
    precio_chat = db.Column(db.Float)
    
    # Datos bancarios
    numero_cuenta = db.Column(db.String(50))
    banco = db.Column(db.String(50))
    titular_cuenta = db.Column(db.String(100))
    
    # Campos de acreditación
    numero_licencia = db.Column(db.String(50))
    institucion = db.Column(db.String(255))
    documento_acreditacion = db.Column(db.String(255))
    informe_certificacion = db.Column(db.String(255))
    
    # Relationship (one-to-many with Especialidad)
    especialidad_id = db.Column(db.Integer, db.ForeignKey('especialidad.id'), nullable=True)
    especialidad = db.relationship('Especialidad', back_populates='psicologos', lazy=True)

    def __repr__(self):
        return f'<Psicologo {self.correo_electronico}>'