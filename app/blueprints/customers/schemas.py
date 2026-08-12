from app.extensions import ma
from app.models import Customer

#==========CUSTOMER SCHEMA==========
# Schemas aid with data validation to prevent server disruption

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        
customer_schema = CustomerSchema() # Serializes a single Customer object
customers_schema = CustomerSchema(many=True) # Serializes a list of Customer objects
login_schema = CustomerSchema(exclude=['name', 'phone'])