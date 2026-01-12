from flask import Blueprint, request, jsonify
from app import db
from app.models import Psicologo, Paciente
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role = data.get('role') # 'psicologo' or 'paciente' - now required to know which table to check
    
    if not role:
        return jsonify({"msg": "Role is required"}), 400

    user = None
    if role == 'psicologo':
        user = Psicologo.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity={'id': user.id_psicologo, 'role': 'psicologo'})
            return jsonify(access_token=access_token, role='psicologo'), 200
            
    elif role == 'paciente':
        user = Paciente.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity={'id': user.id_paciente, 'role': 'paciente'})
            return jsonify(access_token=access_token, role='paciente'), 200
    
    return jsonify({"msg": "Bad username or password"}), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    role = data.get('role')
    
    if role == 'psicologo':
        if Psicologo.query.filter_by(email=data.get('email')).first():
             return jsonify({"msg": "Email already exists"}), 400
        
        new_user = Psicologo(
            nombre=data.get('nombre'),
            email=data.get('email'),
            password_hash=generate_password_hash(data.get('password')),
            telefono=data.get('telefono'),
            especialidad_id=data.get('especialidad_id')
        )
        db.session.add(new_user)
        
    elif role == 'paciente':
        if Paciente.query.filter_by(email=data.get('email')).first():
             return jsonify({"msg": "Email already exists"}), 400
             
        new_user = Paciente(
            nombre=data.get('nombre'),
            email=data.get('email'),
            password_hash=generate_password_hash(data.get('password')),
            apellido=data.get('apellido'),
            edad=data.get('edad'),
            telefono=data.get('telefono'),
            tipo_paciente=data.get('tipo_paciente'),
            tipo_tarjeta=data.get('tipo_tarjeta')
        )
        db.session.add(new_user)
    else:
        return jsonify({"msg": "Invalid role"}), 400
        
    db.session.commit()
    
    return jsonify({"msg": "User created successfully"}), 201

