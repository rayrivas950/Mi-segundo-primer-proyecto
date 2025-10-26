import jwt
from flask import request
from config import Config

def auth_required():
    header = request.headers.get("Authorization")
    if not header:
        return None
    token = header.replace("Bearer ", "")
    try:
        return jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])["user_id"]
    except:
        return None
