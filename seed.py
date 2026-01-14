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
        print("Especialidades added successfully!")

def seed_admin():
    from app.models import Administrador
    from werkzeug.security import generate_password_hash
    with app.app_context():
        # Check if admin already exists
        if Administrador.query.filter_by(correo_electronico='admin@psicologia.com').first():
            print("Admin user already exists.")
            return

        admin = Administrador(
            nombre="Administrador",
            correo_electronico="admin@psicologia.com",
            contrasenia=generate_password_hash("admin123")
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully! (admin@psicologia.com / admin123)")

if __name__ == '__main__':
    seed_especialidades()
    seed_admin()
