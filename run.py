from app import create_app
from app.extensions import db
from app.models import Psicologo, Paciente, Especialidad, Cita, HistorialClinico, Informe, Factura, ResumenIngresos, Notificacion

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 
        'Psicologo': Psicologo,
        'Paciente': Paciente,
        'Especialidad': Especialidad,
        'Cita': Cita,
        'HistorialClinico': HistorialClinico,
        'Informe': Informe,
        'Factura': Factura,
        'ResumenIngresos': ResumenIngresos,
        'Notificacion': Notificacion
    }

if __name__ == '__main__':
    app.run(debug=True)
