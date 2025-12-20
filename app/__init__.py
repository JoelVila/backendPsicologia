# app/__init__.py
from flask import Flask
from config import Config
from app.extensions import init_extensions, db

def init_especialidades(app):
    """Initialize specialties in database if they don't exist"""
    with app.app_context():
        from app.models.Especialidad import Especialidad
        
        # Check if specialties already exist
        if Especialidad.query.first():
            return
        
        especialidades = [
            "Psicología Clínica",
            "Psicología Educativa",
            "Psicología Infantil",
            "Neuropsicología",
            "Psicología Forense",
            "Psicología del Deporte",
            "Psicología Organizacional",
            "Terapia de Pareja",
            "Terapia Familiar",
            "Psicología Geriátrica",
            "Adicciones",
            "Trastornos de Ansiedad",
            "Trastornos del Estado de Ánimo",
            "Trastornos Alimentarios",
            "TDAH",
            "Trauma y TEPT",
            "Mindfulness y Meditación",
            "Coaching Psicológico",
            "Sexología",
            "Duelo y Pérdida"
        ]
        
        for nombre in especialidades:
            nueva = Especialidad(nombre=nombre)
            db.session.add(nueva)
        
        db.session.commit()
        print("✅ 20 especialidades cargadas automáticamente")

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 1. Inicializar Extensiones
    init_extensions(app)

    # 2. Registrar Blueprints
    from app.routes import auth_bp, main_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp, url_prefix='/main')
    
    # 3. Initialize specialties automatically
    init_especialidades(app)

    return app