from extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    refresh_token = db.Column(db.String(255), nullable=True) # Added refresh_token
    created_at = db.Column(db.DateTime, default=datetime.now)
    contacts = db.relationship('Contacto', backref='user', lazy=True, cascade="all, delete-orphan")

class Contacto(db.Model):
    __tablename__ = 'contactos'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    nombre = db.Column(db.String(30), nullable=False)
    image_url = db.Column(db.String(2048), nullable=True)
    notes = db.Column(db.String(150), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    telefonos = db.relationship('Telefono', backref='contacto', lazy=True, cascade="all, delete-orphan")
    emails = db.relationship('Email', backref='contacto', lazy=True, cascade="all, delete-orphan")

class Telefono(db.Model):
    __tablename__ = 'telefonos'
    id = db.Column(db.Integer, primary_key=True)
    contacto_id = db.Column(db.Integer, db.ForeignKey('contactos.id'), nullable=False)
    telefono = db.Column(db.String(255), nullable=False)

class Email(db.Model):
    __tablename__ = 'emails'
    id = db.Column(db.Integer, primary_key=True)
    contacto_id = db.Column(db.Integer, db.ForeignKey('contactos.id'), nullable=False)
    email = db.Column(db.String(50), nullable=False)
