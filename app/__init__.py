# app/__init__.py
from flask import Flask
from config import Config
from app.extensions import init_extensions

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 1. Inicializar Extensiones
    init_extensions(app)

    # 2. Registrar Blueprints
    from app.routes import auth_bp, main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app