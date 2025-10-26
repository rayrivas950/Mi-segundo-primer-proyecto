from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db_connection
import jwt
from datetime import datetime, timedelta
from config import Config

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.post('/register')
def register():
    data = request.json
    username = data["username"]
    password = generate_password_hash(data["password"])
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        return {"message": "Usuario creado"}, 201
    except:
        return {"error": "Usuario ya existe"}, 400
    finally:
        cur.close()

@auth_bp.post('/login')
def login():
    data = request.json
    username = data["username"]
    password = data["password"]

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, password FROM users WHERE username=%s", (username,))
    user = cur.fetchone()
    cur.close()

    if not user or not check_password_hash(user[1], password):
        return {"error": "Credenciales inválidas"}, 401

    token = jwt.encode({"user_id": user[0], "exp": datetime.utcnow() + timedelta(hours=6)}, Config.SECRET_KEY, algorithm="HS256")
    return {"token": token}
