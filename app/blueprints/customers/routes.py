from .schemas import customer_schema, customers_schema, login_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Customer, db, Service_Ticket
from . import customers_bp
from app.extensions import limiter, cache
from app.helpers import get_or_404
from app.utils.util import authenticate_user, token_required
from app.blueprints.service_tickets.schemas import service_tickets_schema


@customers_bp.route('/login', methods=['POST'])
def login():
    return authenticate_user(Customer, login_schema, role='customer')
    
#============CUSTOMER ROUTES===============

# CREATE CUSTOMER (POST / customers Endpoint)
@customers_bp.route('/', methods=['POST'])
@limiter.limit('5 per day') # Prevents bots or others from spamming the API and crashing it by creating a daily limit
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    query = select(Customer).where(Customer.email == customer_data['email'])
    existing_customer = db.session.scalar(query)
    if existing_customer:
        return jsonify({'error': 'Email already associated with an account'}), 400
    
    new_customer = Customer(**customer_data)
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201

# RETRIEVE ALL CUSTOMERS (GET / customers Endpoint)
@customers_bp.route('/', methods=['GET'])
@cache.cached(timeout=60) # Caching this endpoint is important because as the database grows with more customers added, it will become more expensive to gather that data frequently. Caching it allows the return of data to remain fast without exhausting the entire database frequently to retrieve all customers. 
def get_customers():
    query = select(Customer)
    customers = db.session.execute(query).scalars().all()
    
    return customers_schema.jsonify(customers)

# RETREIVE LOGGED-IN CUSTOMER'S SERVICE TICKETS (GET /customers/my-tickets)
@customers_bp.route('/my-tickets', methods=['GET'])
@token_required
def get_my_tickets(user_id, role):
    # Enforce that only customers (not mechanics) access their customer ticket history
    if role != 'customer':
        return jsonify({'message': 'Only customers can access thier personal tickets via this route.'}), 403
    
    query = select(Service_Ticket).where(Service_Ticket.customer_id == user_id)
    tickets = db.session.execute(query).scalars().all()
    
    return service_tickets_schema.jsonify(tickets), 200


# RETRIEVE SPECIFIC CUSTOMER (GET / customers/<id> Endpoint)
@customers_bp.route('/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer, error = get_or_404(Customer, customer_id)
    if error:
        return error
    
    return customer_schema.jsonify(customer), 200

# UPDATE SPECIFIC CUSTOMER (PUT / customers/<id> Endpoint)    
@customers_bp.route('/<int:customer_id>', methods=['PUT'])
@limiter.limit('5 per day') # Limiting updates for a single customer to 5 per day prevents too many visits from a single user and overwhelming the API preventing it from crashing
@token_required
def update_customer(customer_id, user_id, role):
    # Enforce self-edits for customers
    if role == 'customer' and user_id != customer_id:
        return jsonify({'message': 'Unauthorized to modify another account.'}), 403
    customer, error = get_or_404(Customer, customer_id)
    if error:
        return error
    try:
        customer_data = customer_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in customer_data.items():
        setattr(customer, key, value)
    
    db.session.commit()
    return customer_schema.jsonify(customer), 200

# DELETE SPECIFIC CUSTOMER (DELETE / customers/<id> Endpoint)
@customers_bp.route('/<int:customer_id>', methods=['DELETE'])
@limiter.limit('5 per day')
@token_required
def delete_customer(customer_id, user_id, role):
    # Enforce self-edits for customers
    if role == 'customer' and user_id != customer_id:
        return jsonify({'message': 'Unauthorized to delete another account.'}), 403
    customer, error = get_or_404(Customer, customer_id)
    if error:
        return error
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': f'Customer id: {customer_id}, successfully deleted'}), 200

