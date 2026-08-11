from .schemas import service_ticket_schema, service_tickets_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Service_Ticket, Mechanic, db
from . import service_tickets_bp

#=========SERVICE TICKET ROUTES=============

# CREATE SERVICE TICKET (POST /service_tickets Endpoint)
@service_tickets_bp.route('/', methods=['POST'])
def create_service_ticket():
    try:
        service_ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_service_ticket = Service_Ticket(**service_ticket_data)
    db.session.add(new_service_ticket)
    db.session.commit()
    return service_ticket_schema.jsonify(new_service_ticket), 201

# RETRIEVE ALL SERVICE TICKETS (GET /service_tickets Endpoint)
@service_tickets_bp.route('/', methods=['GET'])
def get_service_tickets():
    query = select(Service_Ticket)
    service_tickets = db.session.execute(query).scalars().all()
    
    return service_tickets_schema.jsonify(service_tickets)

# ASSIGN MECHANIC TO SPECIFIC SERVICE TICKET (PUT /service_tickets/<id>/assign-mechanic/<mechanic_id> Endpoint)
@service_tickets_bp.route('/<int:service_ticket_id>/assign-mechanic/<int:mechanic_id>', methods=['PUT'])
def assign_mechanic(service_ticket_id, mechanic_id):
    service_ticket = db.session.get(Service_Ticket, service_ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)
    
    if not service_ticket:
        return jsonify({'error': 'Service Ticket not found'}), 404
    if not mechanic:
        return jsonify({'error': 'Mechanic not found'}), 404
    
    if mechanic in service_ticket.mechanics:
        return jsonify({'message': f'Mechanic id {mechanic_id} is already assigned to this ticket'}), 400
    
    service_ticket.mechanics.append(mechanic)
    db.session.commit()
    
    return jsonify({'message': f'Mechanic id {mechanic_id} successfully assigned to Service Ticket id {service_ticket_id}'}), 200

# REMOVE MECHANIC FROM SERVICE TICKET (PUT /service_tickets/<id>/remove-mechanic<mechanic_id> Endpoint)
@service_tickets_bp.route('/<int:service_ticket_id>/remove-mechanic/<int:mechanic_id>', methods=['PUT'])
def remove_mechanic(service_ticket_id, mechanic_id):
    service_ticket = db.session.get(Service_Ticket, service_ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)
    
    if not service_ticket:
        return jsonify({'error': 'Service Ticket not found'}), 404
    if not mechanic:
        return jsonify({'error': 'Mechanic not found'}), 404
    
    if mechanic not in service_ticket.mechanics:
        return jsonify({'message': f'Mechanic id {mechanic_id} is not assigned to this ticket'}), 400
    
    service_ticket.mechanics.remove(mechanic)
    db.session.commit()
    return jsonify({'message': f'Mechanic id: {mechanic_id}, successfully removed from Service Ticket {service_ticket_id}'}), 200
