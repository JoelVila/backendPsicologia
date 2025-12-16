from flask import Blueprint, request, jsonify
from app.extensions import db

from app.models import Psicologo, Paciente
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
    role = data.get('role') # 'psicologo' or 'paciente'

    if not role:
        return jsonify({"msg": "Role is required"}), 400

    if role == 'psicologo':
        user = Psicologo.query.filter_by(correo_electronico=email).first()
        # Model has 'contrasenia', not 'password_hash'
        if user and check_password_hash(user.contrasenia, password):
            access_token = create_access_token(identity={'id': user.id_psicologo, 'role': 'psicologo'})
            return jsonify(access_token=access_token, role='psicologo'), 200
            
    elif role == 'paciente':
        user = Paciente.query.filter_by(correo_electronico=email).first()
        # Model has 'contrasenia'
        if user and check_password_hash(user.contrasenia, password):
            access_token = create_access_token(identity={'id': user.id_paciente, 'role': 'paciente'})
            return jsonify(access_token=access_token, role='paciente'), 200
    
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
        
        # Psicologo model fields: correo_electronico, contrasenia, informe_certificacion, foto_psicologo, tipo_especialidad, cuenta_bancaria
        # Code was sending: nombre, email, password, telefono, especialidad_id
        # We map what we can.
        new_user = Psicologo(
            correo_electronico=data.get('email'),
            contrasenia=generate_password_hash(data.get('password')),
            tipo_especialidad=str(data.get('especialidad_id')) if data.get('especialidad_id') else None,
            # 'nombre' and 'telefono' are not in Psicologo model, skipping them to avoid crash
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
            tipo_tarjeta=data.get('tipo_tarjeta')
            # 'tipo_paciente' is not in model, skipping
        )
        db.session.add(new_user)
    else:
        return jsonify({"msg": "Invalid role"}), 400
        
    db.session.commit()
    
    return jsonify({"msg": "User created successfully"}), 201

