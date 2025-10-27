from functools import wraps
import jwt
from flask import request
from config import Config
from extensions import is_token_blacklisted # Import the blacklist check

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        header = request.headers.get("Authorization")
        if not header:
            return {"error": "Token inválido o ausente"}, 401
        
        token = header.replace("Bearer ", "")
        
        # Check if token is blacklisted
        if is_token_blacklisted(token):
            return {"error": "Token revocado"}, 401

        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            user_id = payload["user_id"]
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return {"error": "Token inválido o expirado"}, 401
            
        return f(user_id, *args, **kwargs)
    return decorated_function
