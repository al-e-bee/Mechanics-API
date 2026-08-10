from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from decimal import Decimal
from typing import List

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

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        
customer_schema = CustomerSchema() # Serializes a single Customer object
customers_schema = CustomerSchema(many=True) # Serializes a list of Customer objects
    
with app.app_context():
    db.create_all()
    
app.run(debug=True)