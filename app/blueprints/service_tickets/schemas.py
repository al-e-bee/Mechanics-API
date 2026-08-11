from app.extensions import ma
from app.models import Service_Ticket

#==========SERVICE TICKET SCHEMA==========

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Service_Ticket
        include_fk=True
        

# serializes a single Service_Ticket object
service_ticket_schema = ServiceTicketSchema()
# serialized a list of Service_Ticket objects
service_tickets_schema = ServiceTicketSchema(many=True)
