from app import db
from datetime import datetime

class Especialidad(db.Model):
    __tablename__ = 'especialidades'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    # Relationship
    psicologos = db.relationship('Psicologo', backref='especialidad_ref', lazy=True)

class Psicologo(db.Model):
    __tablename__ = 'psicologos'
    id_psicologo = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    telefono = db.Column(db.String(20))
    especialidad_id = db.Column(db.Integer, db.ForeignKey('especialidades.id'))
    
    # Relationships
    citas = db.relationship('Cita', backref='psicologo', lazy=True)
    informes = db.relationship('Informe', backref='psicologo', lazy=True)
    facturas = db.relationship('Factura', backref='psicologo', lazy=True)
    notificaciones = db.relationship('Notificacion', backref='psicologo', lazy=True)
    resumenes_ingresos = db.relationship('ResumenIngresos', backref='psicologo', lazy=True)

class Paciente(db.Model):
    __tablename__ = 'pacientes'
    id_paciente = db.Column(db.Integer, primary_key=True)
    correo_electronico = db.Column(db.String(120), unique=True, nullable=False)
    contrasena = db.Column(db.String(256), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100))
    edad = db.Column(db.Integer)
    telefono = db.Column(db.String(20))
    tipo_paciente = db.Column(db.String(50))
    tipo_tarjeta = db.Column(db.String(50))
    
    # Relationships
    citas = db.relationship('Cita', backref='paciente', lazy=True)
    informes = db.relationship('Informe', backref='paciente', lazy=True)
    facturas = db.relationship('Factura', backref='paciente', lazy=True)
    notificaciones = db.relationship('Notificacion', backref='paciente', lazy=True)
    historial_clinico = db.relationship('HistorialClinico', backref='paciente', uselist=False, cascade="all, delete-orphan")

class Cita(db.Model):
    __tablename__ = 'citas'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    id_paciente = db.Column(db.Integer, db.ForeignKey('pacientes.id_paciente'), nullable=False)
    id_psicologo = db.Column(db.Integer, db.ForeignKey('psicologos.id_psicologo'), nullable=False)
    tipo_cita = db.Column(db.String(50))
    precio_cita = db.Column(db.Float)
    estado = db.Column(db.String(20), default='pendiente')

class Informe(db.Model):
    __tablename__ = 'informes'
    id_informe = db.Column(db.Integer, primary_key=True)
    id_paciente = db.Column(db.Integer, db.ForeignKey('pacientes.id_paciente'), nullable=False)
    id_psicologo = db.Column(db.Integer, db.ForeignKey('psicologos.id_psicologo'), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_modificacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Factura(db.Model):
    __tablename__ = 'facturas'
    id_factura = db.Column(db.Integer, primary_key=True)
    id_paciente = db.Column(db.Integer, db.ForeignKey('pacientes.id_paciente'), nullable=False)
    id_psicologo = db.Column(db.Integer, db.ForeignKey('psicologos.id_psicologo'), nullable=False)
    numero_factura = db.Column(db.String(50), unique=True)
    fecha_emision = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Float) # Kept from previous, usually needed
    pagado = db.Column(db.Boolean, default=False)

class Notificacion(db.Model):
    __tablename__ = 'notificaciones'
    id_notificacion = db.Column(db.Integer, primary_key=True)
    id_paciente = db.Column(db.Integer, db.ForeignKey('pacientes.id_paciente'), nullable=False)
    id_psicologo = db.Column(db.Integer, db.ForeignKey('psicologos.id_psicologo'), nullable=False)
    id_cita = db.Column(db.Integer, db.ForeignKey('citas.id'))
    mensaje = db.Column(db.String(255))
    leida = db.Column(db.Boolean, default=False)

class HistorialClinico(db.Model):
    __tablename__ = 'historiales_clinicos'
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id_paciente'), nullable=False)
    contenido = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

class ResumenIngresos(db.Model):
    __tablename__ = 'resumenes_ingresos'
    id = db.Column(db.Integer, primary_key=True)
    psicologo_id = db.Column(db.Integer, db.ForeignKey('psicologos.id_psicologo'), nullable=False)
    mes = db.Column(db.Integer, nullable=False)
    anio = db.Column(db.Integer, nullable=False)
    total_ingresos = db.Column(db.Float, default=0.0)

