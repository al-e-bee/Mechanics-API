from .schemas import service_ticket_schema, service_tickets_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Service_Ticket, db
from . import service_tickets_bp

#=========SERVICE TICKET ROUTES=============

# CREATE SERVICE TICKET (POST /service_tickets Endpoint)
@service_tickets_bp.route('/', methods=['POST'])
def create_service_ticket():
    try:
        service_ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Service_Ticket).where(Service_Ticket.VIN == service_ticket_data['VIN'])
    existing_service_ticket = db.session.execute(query).scalars().all()
    if existing_service_ticket:
        return jsonify({'error': 'VIN already associated with this service ticket'}), 400
    
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

# RETRIEVE A SINGLE SERVICE TICKET (GET /service_tickets/<id> Endpoint)
@service_tickets_bp.route('/<int:service_ticket_id>', methods=['GET'])
def get_service_ticket(service_ticket_id):
    service_ticket = db.session.get(Service_Ticket, service_ticket_id)
    
    if service_ticket:
        return service_ticket_schema.jsonify(service_ticket)
    return jsonify({'error': 'Service Ticket not found'}), 400

# UPDATE SPECIFIC SERVICE TICKET (PUT /service_tickets/<id> Endpoint)
@service_tickets_bp.route('/<int:service_ticket_id>', methods=['PUT'])
def update_service_ticket(service_ticket_id):
    service_ticket = db.session.get(Service_Ticket, service_ticket_id)
    
    if not service_ticket:
        return jsonify({'error': 'Service Ticket not found'}), 400
    
    try:
        service_ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in service_ticket_data.items():
        setattr(service_ticket, key, value)
        
    db.session.commit()
    return service_ticket_schema.jsonify(service_ticket), 200

# DELETE SERVICE TICKET (DELETE /service_tickets/<id> Endpoint)
@service_tickets_bp.route('/<int:service_ticket_id>', methods=['DELETE'])
def delete_service_ticket(service_ticket_id):
    service_ticket = db.session.get(Service_Ticket, service_ticket_id)
    
    if not service_ticket:
        return jsonify({'error': 'Service Ticket not found'}), 400
    
    db.session.delete(service_ticket)
    db.session.commit()
    return jsonify({'message': f'Service Ticket id: {service_ticket_id}, successfully deleted'}), 200
