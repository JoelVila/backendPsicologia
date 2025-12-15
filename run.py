# run.py
from app import create_app
# Importar el modelo para que Flask-Migrate lo detecte
from app.models.Paciente import Paciente

app = create_app()

if __name__ == '__main__':
    # Usar el modo debug para el desarrollo
    app.run(debug=True)