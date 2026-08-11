from flask import jsonify
from app.extensions import db

def get_or_404(model, item_id):
    item = db.session.get(model, item_id)
    if not item:
        return None, (jsonify({'error': f'{model.__name__} not found'})), 404
    
# Helper function for fetching a record by ID from the database or returns a JSON 404 response. Returns: (instance, None) if found, or (None, response_tuple) if not found.