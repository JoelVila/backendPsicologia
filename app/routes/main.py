from flask import Blueprint, request, jsonify
from app import db
from app.models import Psicologo, Paciente, Cita, Especialidad, HistorialClinico, Informe, Factura, Notificacion
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import json

main_bp = Blueprint('main', __name__)

# --- Psicologos ---
@main_bp.route('/psicologos', methods=['GET'])
@jwt_required()
def get_psicologos():
    psicologos = Psicologo.query.all()
    result = []
    for p in psicologos:
        result.append({
            'id_psicologo': p.id_psicologo,
            'nombre': p.nombre,
            'email': p.email,
            'especialidad': p.especialidad_ref.nombre if p.especialidad_ref else None
        })
    return jsonify(result), 200

# --- Citas ---
@main_bp.route('/citas', methods=['POST'])
@jwt_required()
def create_cita():
    current_user = get_jwt_identity() # Now returns dict {'id': ..., 'role': ...}
    data = request.get_json()
    
    new_cita = Cita(
        fecha=datetime.strptime(data['fecha'], '%Y-%m-%d').date(),
        hora=datetime.strptime(data['hora'], '%H:%M').time(),
        id_psicologo=data['id_psicologo'],
        id_paciente=data['id_paciente'],
        tipo_cita=data.get('tipo_cita'),
        precio_cita=data.get('precio_cita')
    )
    db.session.add(new_cita)
    db.session.commit()
    return jsonify({"msg": "Cita created"}), 201

@main_bp.route('/citas', methods=['GET'])
@jwt_required()
def get_citas():
    citas = Cita.query.all()
    result = []
    for c in citas:
        result.append({
            'id': c.id,
            'fecha': str(c.fecha),
            'hora': str(c.hora),
            'psicologo': c.psicologo.nombre,
            'paciente': c.paciente.nombre,
            'estado': c.estado,
            'tipo_cita': c.tipo_cita,
            'precio_cita': c.precio_cita
        })
    return jsonify(result), 200

# --- Historial Clinico ---
@main_bp.route('/historial/<int:paciente_id>', methods=['GET'])
@jwt_required()
def get_historial(paciente_id):
    historial = HistorialClinico.query.filter_by(paciente_id=paciente_id).first()
    if not historial:
        return jsonify({"msg": "No history found"}), 404
    return jsonify({
        'contenido': historial.contenido,
        'fecha_creacion': historial.fecha_creacion
    }), 200

@main_bp.route('/historial', methods=['POST'])
@jwt_required()
def update_historial():
    data = request.get_json()
    paciente_id = data['id_paciente']
    contenido = data['contenido']
    
    historial = HistorialClinico.query.filter_by(paciente_id=paciente_id).first()
    if historial:
        historial.contenido = contenido
    else:
        historial = HistorialClinico(paciente_id=paciente_id, contenido=contenido)
        db.session.add(historial)
    
    db.session.commit()
    return jsonify({"msg": "Historial updated"}), 200

# --- Informes ---
@main_bp.route('/informes', methods=['POST'])
@jwt_required()
def create_informe():
    data = request.get_json()
    new_informe = Informe(
        id_paciente=data['id_paciente'],
        id_psicologo=data['id_psicologo'],
        contenido=data['contenido']
    )
    db.session.add(new_informe)
    db.session.commit()
    return jsonify({"msg": "Informe created"}), 201

# --- Facturas ---
@main_bp.route('/facturas', methods=['POST'])
@jwt_required()
def create_factura():
    data = request.get_json()
    new_factura = Factura(
        id_paciente=data['id_paciente'],
        id_psicologo=data['id_psicologo'],
        numero_factura=data.get('numero_factura'),
        total=data.get('total')
    )
    db.session.add(new_factura)
    db.session.commit()
    return jsonify({"msg": "Factura created"}), 201

# --- Notificaciones ---
@main_bp.route('/notificaciones', methods=['GET'])
@jwt_required()
def get_notificaciones():
    current_user = get_jwt_identity()
    # Assuming we want notifs for the logged in user.
    # We need to check role to know which field to query
    
    if current_user['role'] == 'paciente':
        notificaciones = Notificacion.query.filter_by(id_paciente=current_user['id']).all()
    elif current_user['role'] == 'psicologo':
        notificaciones = Notificacion.query.filter_by(id_psicologo=current_user['id']).all()
    else:
        return jsonify([]), 200

    result = [{'mensaje': n.mensaje, 'leida': n.leida} for n in notificaciones]
    return jsonify(result), 200

# --- Auth (Paciente) ---
@main_bp.route('/register_paciente', methods=['POST'])
def register_paciente():
    data = request.get_json()
    
    if Paciente.query.filter_by(correo_electronico=data.get('email')).first():
            return jsonify({"msg": "Email already exists"}), 400
            
    new_user = Paciente(
        nombre=data.get('nombre'),
        correo_electronico=data.get('email'),
        contrasena=generate_password_hash(data.get('password')),
        apellido=data.get('apellido'),
        edad=data.get('edad'),
        telefono=data.get('telefono'),
        tipo_paciente=data.get('tipo_paciente'),
        tipo_tarjeta=data.get('tipo_tarjeta')
    )
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"msg": "Paciente created successfully"}), 201

@main_bp.route('/login_paciente', methods=['POST'])
def login_paciente():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    user = Paciente.query.filter_by(correo_electronico=email).first()
    if user and check_password_hash(user.contrasena, password):
        identity_dict = {'id': user.id_paciente, 'role': 'paciente'}
        access_token = create_access_token(identity=json.dumps(identity_dict))
        return jsonify(access_token=access_token, role='paciente'), 200
    
    return jsonify({"msg": "Bad username or password"}), 401

@main_bp.route('/perfil_paciente', methods=['GET'])
@jwt_required()
def perfil_paciente():
    current_user_json = get_jwt_identity()
    try:
        current_user = json.loads(current_user_json)
    except:
        current_user = current_user_json # Fallback if it's already a dict or simple string
        
    if not isinstance(current_user, dict) or current_user.get('role') != 'paciente':
        return jsonify({"msg": "Access denied"}), 403
        
    user = Paciente.query.get(current_user['id'])
    if not user:
        return jsonify({"msg": "User not found"}), 404
        
    return jsonify({
        'id': user.id_paciente,
        'nombre': user.nombre,
        'apellido': user.apellido,
        'email': user.correo_electronico,
        'telefono': user.telefono,
        'edad': user.edad,
        'tipo_paciente': user.tipo_paciente
    }), 200



