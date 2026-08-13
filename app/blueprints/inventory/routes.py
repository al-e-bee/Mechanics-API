from .schemas import inventory_schema, inventories_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Inventory, db
from . import inventory_bp
from app.helpers import get_or_404
from app.utils.util import token_required

#========INVENTORY ROUTES===========

# CREATE INVENTORY ITEM (POST /inventory Endpoint)

@inventory_bp.route('/', methods=['POST'])
def create_inventory():
    try:
        inventory_data =inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Inventory).where(Inventory.name == inventory_data['name'])
    existing_inventory = db.session.scalar(query)
    if existing_inventory:
        return jsonify({'error': 'Inventory item name already in system'}), 400
    
    new_inventory = Inventory(**inventory_data)
    db.session.add(new_inventory)
    db.session.commit()
    return inventory_schema.jsonify(new_inventory), 201

# RETRIEVE ALL INVENTORY ITEMS (GET /inventory Endpoint)
@inventory_bp.route('/', methods=['GET'])
def get_inventory():
    query = select(Inventory)
    inventory_items = db.session.execute(query).scalars().all()
    
    return inventories_schema.jsonify(inventory_items), 200

# RETRIEVE A SINGLE INVENTORY ITEM (GET /inventory/<id> Endpoint)
@inventory_bp.route('/<int:inventory_id>', methods=['GET'])
def get_inventory_item(inventory_id):
    inventory, error = get_or_404(Inventory, inventory_id)
    if error:
        return error
    
    return inventory_schema.jsonify(inventory), 200

# UPDATE SPECIFIC INVENTORY ITEM (PUT /inventory/<id> Endpoint)
@inventory_bp.route('/<int:inventory_id>', methods=['PUT'])
@token_required
def update_inventory(inventory_id, user_id, role):
    if role != 'mechanic':
        return jsonify({'message': 'Mechanic authorization required to update inventory.'}), 403
    inventory, error = get_or_404(Inventory, inventory_id)
    if error:
        return error
    
    try:
        inventory_data = inventory_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in inventory_data.items():
        setattr(inventory, key, value)
        
    db.session.commit()
    return inventory_schema.jsonify(inventory), 200

# DELETE SPECIFIC INVENTORY ITEM (DELETE /inventory/<id> Endpoint)
@inventory_bp.route('/<int:inventory_id>', methods=['DELETE'])
@token_required
def delete_inventory(inventory_id, user_id, role):
    # Restrict action to mechanics to modify inventory
    if role != 'mechanic':
        return jsonify({'message': 'Mechanic authorization required to delete inventory items.'}), 403
    inventory, error = get_or_404(Inventory, inventory_id)
    if error:
        return error
    
    db.session.delete(inventory)
    db.session.commit()
    return jsonify({'message': f'Inventory id: {inventory_id}, successfully deleted'}), 200

