from app.extensions import ma
from app.models import Service_Ticket

#==========SERVICE TICKET SCHEMA==========

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Service_Ticket
        include_fk=True
    # Nested Relationships included so they show up in JSON
    parts = ma.Nested('InventorySchema', many=True)
    mechanics = ma.Nested('MechanicSchema', many=True, exclude=('email','phone','password', 'salary'))
    
# serializes a single Service_Ticket object
service_ticket_schema = ServiceTicketSchema()
# serialized a list of Service_Ticket objects
service_tickets_schema = ServiceTicketSchema(many=True)
