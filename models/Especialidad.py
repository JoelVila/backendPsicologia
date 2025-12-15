# app/models/especialidad.py
from app.extensions import db


class Especialidad(db.Model):
    __tablename__ = 'especialidad'

    # Se usa una clave compuesta según el diagrama (id_especialidad y tipo_especialidad)
    # Sin embargo, id_especialidad es más común para ser PK única.
    # Usaremos solo id_especialidad como PK y combinaremos las claves en el modelo
    id_especialidad = db.Column(db.Integer, primary_key=True)
    # FK:
    id_psicologo = db.Column(db.Integer)

    tipo_especialidad = db.Column(db.String(100))

    def __repr__(self):
        return f'<Especialidad {self.tipo_especialidad}>'