from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Psicologo, Paciente, Administrador
from app.models.Especialidad import Especialidad
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if isinstance(data, list):
        data = data[0] if len(data) > 0 else {}
    
    email = data.get('email')
    password = data.get('password')
    role = data.get('role') # 'psicologo', 'paciente' or 'admin'

    if not role:
        return jsonify({"msg": "Role is required"}), 400

    if role == 'psicologo':
        user = Psicologo.query.filter_by(correo_electronico=email).first()
        if user and check_password_hash(user.contrasenia, password):
            access_token = create_access_token(identity={'id': user.id_psicologo, 'role': 'psicologo'})
            return jsonify(access_token=access_token, role='psicologo'), 200
            
    elif role == 'paciente':
        user = Paciente.query.filter_by(correo_electronico=email).first()
        if user and check_password_hash(user.contrasenia, password):
            access_token = create_access_token(identity={'id': user.id_paciente, 'role': 'paciente'})
            return jsonify(access_token=access_token, role='paciente'), 200

    elif role == 'admin':
        user = Administrador.query.filter_by(correo_electronico=email).first()
        if user and check_password_hash(user.contrasenia, password):
            access_token = create_access_token(identity={'id': user.id_admin, 'role': 'admin'})
            return jsonify(access_token=access_token, role='admin'), 200
    
    return jsonify({"msg": "Bad username or password"}), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if isinstance(data, list):
        data = data[0] if len(data) > 0 else {}
    
    role = data.get('role')
    
    if role == 'psicologo':
        if Psicologo.query.filter_by(correo_electronico=data.get('email')).first():
             return jsonify({"msg": "Email already exists"}), 400
        
        # Handle specialty (can be ID or Name/Tag)
        especialidad_input = data.get('especialidad_id')
        target_especialidad_id = None
        
        if isinstance(especialidad_input, int):
            target_especialidad_id = especialidad_input
        elif isinstance(especialidad_input, str):
            # If it's a string, look up the ID by specialty name
            esp = Especialidad.query.filter_by(nombre=especialidad_input).first()
            if esp:
                target_especialidad_id = esp.id

        # --- Verificación de Seguridad contra el COPC ---
        num_licencia = data.get('numero_licencia')
        if not num_licencia:
             return jsonify({"msg": "Registration failed: License number is required for verification."}), 400
             
        from app.utils.verification_copc import verify_psicologo_copc
        verification = verify_psicologo_copc(num_licencia)
        if not verification.get("verified"):
            return jsonify({"msg": f"Registration denied: {verification.get('msg')}"}), 403
            
        # Usar datos verificados para mayor precisión
        nombre_final = verification.get("nombre") or data.get('nombre')
        licencia_final = verification.get("numero_colegiado") or num_licencia
        institucion_final = "COPC (Catalunya)" if verification.get("verified") else data.get('institucion')
        # -----------------------------------------------

        new_user = Psicologo(
            nombre=nombre_final,
            correo_electronico=data.get('email'),
            contrasenia=generate_password_hash(data.get('password')),
            numero_licencia=licencia_final,
            institucion=institucion_final,
            documento_acreditacion=data.get('documento_acreditacion'),
            foto_psicologo=data.get('foto_psicologo'),
            especialidad_id=target_especialidad_id,
            verificado=verification.get("verified", False)
        )
        db.session.add(new_user)
        
    elif role == 'paciente':
        if Paciente.query.filter_by(correo_electronico=data.get('email')).first():
             return jsonify({"msg": "Email already exists"}), 400
             
        # Paciente model: correo_electronico, contrasenia, nombre_completo, edad, telefono, foto_paciente, tipo_tarjeta
        nombre = data.get('nombre', '')
        apellido = data.get('apellido', '')
        nombre_completo = f"{nombre} {apellido}".strip()

        new_user = Paciente(
            nombre_completo=nombre_completo,
            correo_electronico=data.get('email'),
            contrasenia=generate_password_hash(data.get('password')),
            edad=data.get('edad'),
            telefono=data.get('telefono'),
            tipo_tarjeta=data.get('tipo_tarjeta'),
            foto_paciente=data.get('foto_paciente')
            # 'tipo_paciente' is not in model, skipping
        )
        db.session.add(new_user)
    else:
        return jsonify({"msg": "Invalid role"}), 400
        
    db.session.commit()
    
    return jsonify({"msg": "User created successfully"}), 201

@auth_bp.route('/especialidades', methods=['GET'])
def get_especialidades():
    """Get all available specialties"""
    especialidades = Especialidad.query.all()
    return jsonify([
        {'id': esp.id, 'nombre': esp.nombre}
        for esp in especialidades
    ]), 200

