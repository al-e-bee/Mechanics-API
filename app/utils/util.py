import os
import jwt
from datetime import datetime, timezone, timedelta
from functools import wraps
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import db



SECRET_KEY = os.environ.get('SECRET_KEY') or "super secret secrets"

# Login Function
def authenticate_user(model, login_schema, role):
    try:
        credentials = login_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    email = credentials['email']
    password = credentials['password']
    
    # Query the provided model
    query = select(model).where(model.email == email)
    user = db.session.scalar(query)
    
    # Validate user existence and direct string password match
    if not user or user.password != password:
        return jsonify({'message': 'Invalid email or password!'}), 401
    
    # Generate token using the user's ID and role
    token = encode_token(user.id, role=role)
    
    return jsonify({
        "status": "success",
        "message": "Successfully logged in.",
        "token": token
    }), 200

# Encode Token Function
def encode_token(user_id, role='customer'):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=0, hours=1),
        'iat': datetime.now(timezone.utc),
        'sub': str(user_id), 
        'role': role
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

# Decorated Function for Token Authentication
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # 1. Extract Authorization Header safely
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'message': 'You must be logged in to access this info.'}), 401
        
        try:
            # Safely split 'Bearer <token>'
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == 'bearer':
                token = parts[1]
            else:
                token = parts[0] # Fallback if raw token was sent without 'Bearer'
        except Exception:
            return jsonify({'message': 'Invalid token format'}), 401
        
        # 2. Decode & Validate Token
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            user_id = int(data['sub'])
            role = data.get('role', 'customer')
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError as e:
            print('JWT DECODE ERROR REASON:', repr(e))
            return jsonify({'message': 'Invalid token'}), 401
        
        # 3. Pass user info down to the route
        return f(user_id=user_id, role=role, *args, **kwargs)
    
    return decorated