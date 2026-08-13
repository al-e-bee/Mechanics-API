from .schemas import mechanic_schema, mechanics_schema, login_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select, func
from app.models import Mechanic, db, Service_Ticket
from . import mechanics_bp
from app.helpers import get_or_404
from app.utils.util import authenticate_user, token_required


@mechanics_bp.route('/login', methods=['POST'])
def login():
    return authenticate_user(Mechanic, login_schema, role='mechanic')
#=======MECHANIC ROUTES========

# CREATE MECHANIC (POST /mechanics Endpoint)

@mechanics_bp.route('/', methods=['POST'])
def create_mechanic():
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Mechanic).where(Mechanic.email == mechanic_data['email'])
    existing_mechanic = db.session.scalar(query)
    if existing_mechanic:
        return jsonify({'error': 'Email already associated with an account'}), 400
    
    new_mechanic = Mechanic(**mechanic_data)
    db.session.add(new_mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(new_mechanic), 201


# RETRIEVE ALL MECHANICS (GET /mechanics Endpoint)
@mechanics_bp.route('/', methods=['GET'])
def get_mechanics():
    query = select(Mechanic)
    mechanics = db.session.execute(query).scalars().all()
    
    return mechanics_schema.jsonify(mechanics)

# POPULAR MECHANICS (GET /mechanics/top-performers)
@mechanics_bp.route('/top-performers', methods=['GET'])
def get_top_mechanics():
    # Outer join mechanic to their service tickets relationship, count tickets, and order descending
    query = (
        select(Mechanic)
        .outerjoin(Mechanic.services)
        .group_by(Mechanic.id)
        .order_by(func.count(Service_Ticket.id).desc())
    )
    
    top_mechanics = db.session.scalars(query).all()
    return mechanics_schema.jsonify(top_mechanics), 200

# RETRIEVE A SINGLE MECHANIC (GET /mechanics/<id> Endpoint)
@mechanics_bp.route('/<int:mechanic_id>', methods=['GET'])
def get_mechanic(mechanic_id):
    mechanic, error = get_or_404(Mechanic, mechanic_id)
    if error:
        return error
    
    return mechanic_schema.jsonify(mechanic), 200
    

# UPDATE SPECIFIC MECHANIC (PUT /mechanics/<id> Endpoint)
@mechanics_bp.route('/<int:mechanic_id>', methods=['PUT'])
@token_required
def update_mechanic(mechanic_id, user_id, role):
    if role == 'mechanic' and user_id != mechanic_id:
        return jsonify({'message': 'Unauthorized to modify another mechanic profile'}), 403
    mechanic, error = get_or_404(Mechanic, mechanic_id)
    if error:
        return error
    
    try:
        mechanic_data = mechanic_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in mechanic_data.items():
        setattr(mechanic, key, value)
        
    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200

# DELETE SPECIFIC MECHANIC (DELETE /mechanics/<id> Endpoint)
@mechanics_bp.route('/<int:mechanic_id>', methods=['DELETE'])
@token_required
def delete_mechanic(mechanic_id, user_id, role):
    # Restrict action to mechanics modifying their own profile
    if role == 'mechanic' and user_id != mechanic_id:
        return jsonify({'message': 'Unauthorized to delete another mechanic profile.'}), 403
    mechanic, error = get_or_404(Mechanic, mechanic_id)
    if error:
        return error
    
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({'message': f'Mechanic id: {mechanic_id}, successfully deleted'}), 200

