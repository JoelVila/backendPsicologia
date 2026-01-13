from app import create_app, db
from app.models import Especialidad

app = create_app()

def seed_especialidades():
    with app.app_context():
        # Check if specialties exist
        # Removed the early return to allow adding new specialties to an existing list
        # if Especialidad.query.first():
        #     print("Especialidades already exist.")
        #     return

        especialidades = [
            "Psicología Clínica",
            "Psicología Educativa",
            "Psicología Infantil y Juvenil",
            "Neuropsicología",
            "Psicología Forense",
            "Psicología del Deporte",
            "Psicología de la Salud",
            "Psicología Organizacional",
            "Psicología Social",
            "Psicología Familiar y de Pareja",
            "Psicología Cognitivo-Conductual",
            "Psicoanálisis",
            "Psicología Humanista",
            "Sexología",
            "Psicogerontología",
            "Psicología de las Adicciones",
            "Coaching Psicológico"
        ]

        for nombre in especialidades:
            if not Especialidad.query.filter_by(nombre=nombre).first():
                nueva = Especialidad(nombre=nombre)
                db.session.add(nueva)
                print(f"Adding: {nombre}")
        
        db.session.commit()
        print("Especialidades added successfully!")

if __name__ == '__main__':
    seed_especialidades()
