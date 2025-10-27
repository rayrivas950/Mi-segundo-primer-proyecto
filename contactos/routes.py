from flask import Blueprint, request, jsonify
from sqlalchemy.orm import joinedload
from sqlalchemy import or_
from extensions import db
from models import Contacto, Telefono, Email
from .auth_guard import auth_required
from .schemas import contacto_schema, contactos_schema # Import schemas
from marshmallow import ValidationError # Import ValidationError

contactos_bp = Blueprint('contactos', __name__, url_prefix='/contactos')

@contactos_bp.post('/')
@auth_required
def crear(user_id):
    try:
        # Validate and deserialize input data into a Contacto instance
        nuevo_contacto = contacto_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    nuevo_contacto.user_id = user_id # Assign user_id from auth_required

    db.session.add(nuevo_contacto)
    db.session.commit()

    # Serialize the created contact for the response
    return contacto_schema.dump(nuevo_contacto), 201


@contactos_bp.get('/')
@auth_required
def obtener_contactos(user_id):
    search_query = request.args.get("search")

    query = Contacto.query.filter_by(user_id=user_id).options(
        joinedload(Contacto.telefonos),
        joinedload(Contacto.emails)
    )

    if search_query:
        search_pattern = f"%{search_query}%"
        query = query.join(Contacto.telefonos, isouter=True).join(Contacto.emails, isouter=True).filter(
            or_(
                Contacto.nombre.ilike(search_pattern),
                Telefono.telefono.ilike(search_pattern),
                Email.email.ilike(search_pattern)
            )
        ).distinct()

    contactos_db = query.order_by(Contacto.nombre).all()

    # Serialize the list of contacts
    return contactos_schema.dump(contactos_db), 200


@contactos_bp.put('/<int:contact_id>')
@auth_required
def actualizar_contacto(user_id, contact_id):
    contacto = Contacto.query.filter_by(id=contact_id, user_id=user_id).first_or_404(
        description="Contacto no encontrado o no pertenece al usuario"
    )

    try:
        # Update the existing contact instance with validated data
        # partial=True allows for partial updates (not all fields required)
        updated_contacto = contacto_schema.load(request.json, instance=contacto, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    db.session.commit()
    # Serialize the updated contact for the response
    return contacto_schema.dump(updated_contacto), 200


@contactos_bp.delete('/<int:contact_id>')
@auth_required
def eliminar_contacto(user_id, contact_id):
    contacto = Contacto.query.filter_by(id=contact_id, user_id=user_id).first_or_404(
        description="Contacto no encontrado o no pertenece al usuario"
    )

    db.session.delete(contacto)
    db.session.commit()

    return {"message": "Contacto eliminado"}, 200
