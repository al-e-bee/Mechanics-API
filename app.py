from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from decimal import Decimal
from typing import List
from marshmallow import ValidationError
from sqlalchemy import select


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:*D3tr01t26!*@localhost/mechanic_api'

# Create a base class for the models
class Base(DeclarativeBase):
    pass

# Initiate the SQLAlchemy database
db = SQLAlchemy(model_class = Base)
ma = Marshmallow()

db.init_app(app) # adding the db extension to the app
ma.init_app(app) # adding Marshmallow to the app

service_mechanics = db.Table(
    'service_mechanics',
    Base.metadata,
    db.Column('service_ticket_id', db.ForeignKey('service_tickets.id')),
    db.Column('mechanic_id', db.ForeignKey('mechanics.id'))
)

#=============CLASS MODELS========================

class Customer(Base):
    __tablename__='customers'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(50), nullable=False)
    
    tickets: Mapped[List['Service_Ticket']] = relationship(back_populates='customer')
    
class Service_Ticket(Base):
    __tablename__='service_tickets'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    VIN: Mapped[str] = mapped_column(db.String(50), nullable=False)
    service_date: Mapped[str] = mapped_column(db.String(100), nullable=False)
    service_desc: Mapped[str] = mapped_column(db.String(360), nullable=False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.id'))
    
    customer: Mapped['Customer'] = relationship(back_populates='tickets')
    mechanics: Mapped[List['Mechanic']] = relationship(secondary=service_mechanics, back_populates='services')
    
class Mechanic(Base):
    __tablename__='mechanics'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(50), nullable=False)
    salary: Mapped[Decimal] = mapped_column(db.Numeric(10, 2), nullable=False)

    services: Mapped[List['Service_Ticket']] = relationship(secondary=service_mechanics, back_populates='mechanics')
    
    
    
#============SCHEMAS============
# Schemas aid with data validation to prevent server disruption

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        
customer_schema = CustomerSchema() # Serializes a single Customer object
customers_schema = CustomerSchema(many=True) # Serializes a list of Customer objects


#============ROUTES===============

# CREATE CUSTOMER (POST / customers Endpoint)
@app.route('/customers', methods=['POST'])
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    query = select(Customer).where(Customer.email == customer_data['email'])
    existing_customer = db.session.execute(query).scalars().all()
    if existing_customer:
        return jsonify({'error': 'Email already associated with an account'}), 400
    
    new_customer = Customer(**customer_data)
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201

# RETRIEVE ALL CUSTOMERS (GET / customers Endpoint)
@app.route('/customers', methods=['GET'])
def get_customers():
    query = select(Customer)
    customers = db.session.execute(query).scalars().all()
    
    return customers_schema.jsonify(customers)

# RETRIEVE SPECIFIC CUSTOMER (GET / customers/<id> Endpoint)
@app.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    
    if customer:
        return customer_schema.jsonify(customer)
    return jsonify({'error': "Customer not found"}), 400

# UPDATE SPECIFIC CUSTOMER (PUT / customers/<id> Endpoint)    
@app.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    
    if not customer:
        return jsonify({'error': "Customer not found"}), 400
    
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in customer_data.items():
        setattr(customer, key, value)
    
    db.session.commit()
    return customer_schema.jsonify(customer), 200

# DELETE SPECIFIC CUSTOMER (DELETE / customers/<id> Endpoint)
@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    
    if not customer:
        return jsonify({'error': 'Customer not found.'}), 400
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': f'Customer id: {customer_id}, successfully deleted'}), 200



    
with app.app_context():
    db.create_all()
    
app.run(debug=True)