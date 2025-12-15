# app/__init__.py
from flask import Flask
from config import Config
from app.extensions import init_extensions

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 1. Inicializar Extensiones
    init_extensions(app)

    # 2. Registrar Blueprints (Se añadirán después)
    # from app.api.paciente_routes import bp as paciente_bp
    # app.register_blueprint(paciente_bp, url_prefix='/api/v1/pacientes')

    return app


def models():
    return None