from app.extensions import ma
from app.models import Mechanic

#=======MECHANIC SCHEMA=======

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic

# serializes a single Mechanic object       
mechanic_schema = MechanicSchema()
# Serializes a list of Mechanic objects
mechanics_schema = MechanicSchema(many=True)