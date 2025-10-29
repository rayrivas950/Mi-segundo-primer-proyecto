from flask import Blueprint, request, jsonify # Added jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta, timezone
from config import Config
from extensions import limiter, db, add_token_to_blacklist
from models import User
from contactos.auth_guard import auth_required
import uuid
from marshmallow import ValidationError # Added ValidationError
from .schemas import user_register_schema, user_login_schema # Added auth schemas

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.post('/register')
@limiter.limit("5 per hour")
def register():
    try:
        data = user_register_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    username = data["username"].lower()
    password = generate_password_hash(data["password"])

    new_user = User(username=username, password=password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return {"message": "Usuario creado"}, 201
    except IntegrityError:
        db.session.rollback()
        return {"error": "Usuario ya existe"}, 400

@auth_bp.post('/login')
@limiter.limit("10 per minute")
def login():
    try:
        data = user_login_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    username = data["username"].lower()
    password = data["password"]

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return {"error": "Credenciales inválidas"}, 401

    # Generate access token (short-lived)
    access_token = jwt.encode(
        {"user_id": user.id, "exp": datetime.now(timezone.utc) + timedelta(minutes=15)}, # Shorter expiration
        Config.SECRET_KEY,
        algorithm="HS256"
    )

    # Generate and store refresh token (long-lived)
    refresh_token = str(uuid.uuid4())
    user.refresh_token = refresh_token
    db.session.commit()

    return {"access_token": access_token, "refresh_token": refresh_token}

@auth_bp.post('/logout')
@auth_required
def logout(user_id):
    header = request.headers.get("Authorization")
    token = header.replace("Bearer ", "")
    add_token_to_blacklist(token)
    return {"message": "Sesión cerrada exitosamente"}, 200

@auth_bp.post('/refresh')
@limiter.limit("5 per minute") # Limit refresh attempts
def refresh():
    data = request.json
    refresh_token = data.get("refresh_token")

    if not refresh_token:
        return {"error": "Refresh token ausente"}, 401

    user = User.query.filter_by(refresh_token=refresh_token).first()

    if not user:
        return {"error": "Refresh token inválido"}, 401

    # Generate new access token
    new_access_token = jwt.encode(
        {"user_id": user.id, "exp": datetime.now(timezone.utc) + timedelta(minutes=15)},
        Config.SECRET_KEY,
        algorithm="HS256"
    )

    # Generate new refresh token (rotation)
    new_refresh_token = str(uuid.uuid4())
    user.refresh_token = new_refresh_token
    db.session.commit()

    return {"access_token": new_access_token, "refresh_token": new_refresh_token}
