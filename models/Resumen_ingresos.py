# app/models/resumen_ingresos.py
from app.extensions import db


class ResumenIngresos(db.Model):
    __tablename__ = 'resumen_ingresos'

    # Usamos un ID propio como PK más estándar, aunque el diagrama sugiere id_informe como PK
    id_resumen = db.Column(db.Integer, primary_key=True)
    id_informe = db.Column(db.Integer, unique=True)  # Como FK o referencia
    # FK:
    id_psicologo = db.Column(db.Integer)

    ingresos_totales = db.Column(db.Numeric(10, 2))
    pacientes_atendidos = db.Column(db.Integer)
    promedio_sesion = db.Column(db.Numeric(10, 2))
    sesiones_completas = db.Column(db.Integer)

    def __repr__(self):
        return f'<Resumen {self.id_resumen} Psicólogo: {self.id_psicologo}>'