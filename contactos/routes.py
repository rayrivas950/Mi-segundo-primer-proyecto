from flask import Blueprint, request
from db import get_db_connection
from .auth_guard import auth_required

contactos_bp = Blueprint('contactos', __name__, url_prefix='/contactos')

@contactos_bp.post('/')
def crear():
    user_id = auth_required()
    if not user_id:
        return {"error": "Token inválido"}, 401

    data = request.json
    nombre = data["nombre"]
    telefonos = data.get("telefonos", [])
    emails = data.get("emails", [])

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO contactos (user_id, nombre) VALUES (%s, %s) RETURNING id", (user_id, nombre))
    cid = cur.fetchone()[0]

    for t in telefonos:
        cur.execute("INSERT INTO telefonos (contacto_id, telefono) VALUES (%s, %s)", (cid, t))

    for e in emails:
        cur.execute("INSERT INTO emails (contacto_id, email) VALUES (%s, %s)", (cid, e))

    conn.commit()
    cur.close()
    return {"message": "Contacto creado"}, 201


@contactos_bp.get('/')
def obtener_contactos():
    user_id = auth_required()
    if not user_id:
        return {"error": "Token inválido"}, 401

    search_query = request.args.get("search")

    conn = get_db_connection()
    cur = conn.cursor()

    if search_query:
        search_pattern = f"%{search_query}%"
        cur.execute(
            """SELECT DISTINCT c.id, c.nombre FROM contactos c
            LEFT JOIN telefonos t ON c.id = t.contacto_id
            LEFT JOIN emails e ON c.id = e.contacto_id
            WHERE c.user_id = %s AND (c.nombre ILIKE %s OR t.telefono ILIKE %s OR e.email ILIKE %s)
            ORDER BY c.nombre""",
            (user_id, search_pattern, search_pattern, search_pattern)
        )
    else:
        cur.execute("SELECT id, nombre FROM contactos WHERE user_id = %s ORDER BY nombre", (user_id,))
    
    contactos_db = cur.fetchall()

    contactos = []
    for contacto_id, nombre in contactos_db:
        cur.execute("SELECT telefono FROM telefonos WHERE contacto_id = %s", (contacto_id,))
        telefonos = [t[0] for t in cur.fetchall()]

        cur.execute("SELECT email FROM emails WHERE contacto_id = %s", (contacto_id,))
        emails = [e[0] for e in cur.fetchall()]

        contactos.append({
            "id": contacto_id,
            "nombre": nombre,
            "telefonos": telefonos,
            "emails": emails
        })
    
    cur.close()
    return {"contactos": contactos}

@contactos_bp.put('/<int:contact_id>')
def actualizar_contacto(contact_id):
    user_id = auth_required()
    if not user_id:
        return {"error": "Token inválido"}, 401

    data = request.json
    nombre = data.get("nombre")
    telefonos = data.get("telefonos", [])
    emails = data.get("emails", [])

    conn = get_db_connection()
    cur = conn.cursor()

    # Check if contact exists and belongs to the user
    cur.execute("SELECT id FROM contactos WHERE id = %s AND user_id = %s", (contact_id, user_id))
    if not cur.fetchone():
        cur.close()
        return {"error": "Contacto no encontrado o no pertenece al usuario"}, 404

    # Update contact name
    if nombre:
        cur.execute("UPDATE contactos SET nombre = %s WHERE id = %s", (nombre, contact_id))

    # Update phones (delete existing, insert new)
    cur.execute("DELETE FROM telefonos WHERE contacto_id = %s", (contact_id,))
    for t in telefonos:
        cur.execute("INSERT INTO telefonos (contacto_id, telefono) VALUES (%s, %s)", (contact_id, t))

    # Update emails (delete existing, insert new)
    cur.execute("DELETE FROM emails WHERE contacto_id = %s", (contact_id,))
    for e in emails:
        cur.execute("INSERT INTO emails (contacto_id, email) VALUES (%s, %s)", (contact_id, e))

    conn.commit()
    cur.close()
    return {"message": "Contacto actualizado"}, 200

@contactos_bp.delete('/<int:contact_id>')
def eliminar_contacto(contact_id):
    user_id = auth_required()
    if not user_id:
        return {"error": "Token inválido"}, 401

    conn = get_db_connection()
    cur = conn.cursor()

    # Check if contact exists and belongs to the user
    cur.execute("SELECT id FROM contactos WHERE id = %s AND user_id = %s", (contact_id, user_id))
    if not cur.fetchone():
        cur.close()
        return {"error": "Contacto no encontrado o no pertenece al usuario"}, 404

    cur.execute("DELETE FROM contactos WHERE id = %s", (contact_id,))
    conn.commit()
    cur.close()
    return {"message": "Contacto eliminado"}, 200

