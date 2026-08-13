from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from decimal import Decimal
from typing import List
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
# from .extensions import db

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Junction Table 1: Service Tickets <-> Mechanics
service_mechanics = db.Table(
    'service_mechanics',
    Base.metadata,
    db.Column('service_ticket_id', db.ForeignKey('service_tickets.id')),
    db.Column('mechanic_id', db.ForeignKey('mechanics.id'))
)

# Junction Table 2: Service Tickets <-> Inventory Parts
service_inventory = db.Table(
    'service_inventory_parts',
    Base.metadata,
    db.Column('service_ticket_id', db.ForeignKey('service_tickets.id')),
    db.Column('inventory_id', db.ForeignKey('inventory.id'))
)

#=============CLASS MODELS========================

class Customer(Base):
    __tablename__='customers'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(db.String(200), nullable=False)
    phone: Mapped[str] = mapped_column(db.String(50), nullable=False)
    
    tickets: Mapped[List['Service_Ticket']] = relationship(back_populates='customer')
    
class Service_Ticket(Base):
    __tablename__='service_tickets'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    VIN: Mapped[str] = mapped_column(db.String(50), nullable=False)
    service_date: Mapped[str] = mapped_column(db.String(100), nullable=False)
    service_desc: Mapped[str] = mapped_column(db.String(360), nullable=False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.id'), nullable=False)
    
    customer: Mapped['Customer'] = relationship(back_populates='tickets')
    mechanics: Mapped[List['Mechanic']] = relationship(secondary=service_mechanics, back_populates='services')
    
    # Many-to-Many with Inventory
    parts: Mapped[List['Inventory']] = relationship(secondary=service_inventory, back_populates='service_tickets')
    
class Mechanic(Base):
    __tablename__='mechanics'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(db.String(200), nullable=False)
    phone: Mapped[str] = mapped_column(db.String(50), nullable=False)
    salary: Mapped[Decimal] = mapped_column(db.Numeric(10, 2), nullable=False)

    services: Mapped[List['Service_Ticket']] = relationship(secondary=service_mechanics, back_populates='mechanics')
    
class Inventory(Base):
    __tablename__ = 'inventory'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(300), nullable=False)
    price: Mapped[float] = mapped_column(db.Float, nullable=False)
    
    # Many-to-Many  back to Service_Ticket
    service_tickets: Mapped[List['Service_Ticket']] = relationship(secondary=service_inventory, back_populates='parts')