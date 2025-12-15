from app import create_app, db
from app.models import Especialidad

app = create_app()

def seed_especialidades():
    with app.app_context():
        # Check if specialties exist
        if Especialidad.query.first():
            print("Especialidades already exist.")
            return

        especialidades = [
            "Psicología Clínica",
            "Psicología Educativa",
            "Psicología Infantil",
            "Neuropsicología",
            "Psicología Forense",
            "Psicología del Deporte"
        ]

        for nombre in especialidades:
            nueva = Especialidad(nombre=nombre)
            db.session.add(nueva)
        
        db.session.commit()
        print("Especialidades added successfully!")

if __name__ == '__main__':
    seed_especialidades()
