from app.extensions import ma
from app.models import Inventory

#========INVENTORY SCHEMA=========

class InventorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory
        
# serializes a single Inventory object
inventory_schema = InventorySchema()
# serializes a list of Inventory objects
inventories_schema = InventorySchema(many=True)