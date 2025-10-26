import pytest
from app import app
from db import create_tables, get_db_connection
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.app_context():
        create_tables()
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM users")
        cur.execute("DELETE FROM contactos")
        cur.execute("DELETE FROM telefonos")
        cur.execute("DELETE FROM emails")
        conn.commit()
        cur.close()
    with app.test_client() as client:
        yield client

@pytest.fixture
def auth_client(client):
    # Register a user
    register_data = {"username": "testuser", "password": "testpassword"}
    client.post('/auth/register', json=register_data)

    # Log in and get token
    login_data = {"username": "testuser", "password": "testpassword"}
    response = client.post('/auth/login', json=login_data)
    token = json.loads(response.data)["token"]

    return client, token

def test_create_contact(auth_client):
    client, token = auth_client
    headers = {'Authorization': f'Bearer {token}'}
    contact_data = {"nombre": "Alice", "telefonos": ["111-222-3333"], "emails": ["alice@example.com"]}
    response = client.post('/contactos/', headers=headers, json=contact_data)
    assert response.status_code == 201
    assert json.loads(response.data)["message"] == "Contacto creado"

def test_create_contact_unauthorized(client):
    contact_data = {"nombre": "Alice", "telefonos": ["111-222-3333"], "emails": ["alice@example.com"]}
    response = client.post('/contactos/', json=contact_data)
    assert response.status_code == 401
    assert json.loads(response.data)["error"] == "Token inválido"

def test_get_contacts(auth_client):
    client, token = auth_client
    headers = {'Authorization': f'Bearer {token}'}

    # Create a contact first
    contact_data = {"nombre": "Bob", "telefonos": ["444-555-6666"], "emails": ["bob@example.com"]}
    client.post('/contactos/', headers=headers, json=contact_data)

    response = client.get('/contactos/', headers=headers)
    assert response.status_code == 200
    contacts = json.loads(response.data)["contactos"]
    assert len(contacts) == 1
    assert contacts[0]["nombre"] == "Bob"

def test_search_contacts(auth_client):
    client, token = auth_client
    headers = {'Authorization': f'Bearer {token}'}

    # Create contacts for searching
    client.post('/contactos/', headers=headers, json={
        "nombre": "Charlie", "telefonos": ["123-456-7890"], "emails": ["charlie@example.com"]})
    client.post('/contactos/', headers=headers, json={
        "nombre": "David", "telefonos": ["987-654-3210"], "emails": ["david@test.com"]})

    # Search by name
    response = client.get('/contactos/?search=Charlie', headers=headers)
    assert response.status_code == 200
    contacts = json.loads(response.data)["contactos"]
    assert len(contacts) == 1
    assert contacts[0]["nombre"] == "Charlie"

    # Search by phone
    response = client.get('/contactos/?search=987', headers=headers)
    assert response.status_code == 200
    contacts = json.loads(response.data)["contactos"]
    assert len(contacts) == 1
    assert contacts[0]["nombre"] == "David"

    # Search by email
    response = client.get('/contactos/?search=charlie@example.com', headers=headers)
    assert response.status_code == 200
    contacts = json.loads(response.data)["contactos"]
    assert len(contacts) == 1
    assert contacts[0]["nombre"] == "Charlie"

def test_update_contact(auth_client):
    client, token = auth_client
    headers = {'Authorization': f'Bearer {token}'}

    # Create a contact to update
    create_response = client.post('/contactos/', headers=headers, json={
        "nombre": "Eve", "telefonos": ["111-222-3333"], "emails": ["eve@example.com"]})
    contact_id = json.loads(create_response.data)["id"] # Assuming the POST returns the ID

    # Update the contact
    update_data = {"nombre": "Eva", "telefonos": ["555-123-4567"], "emails": ["eva.new@example.com"]}
    response = client.put(f'/contactos/{contact_id}', headers=headers, json=update_data)
    assert response.status_code == 200
    assert json.loads(response.data)["message"] == "Contacto actualizado"

    # Verify the update
    get_response = client.get('/contactos/', headers=headers)
    contacts = json.loads(get_response.data)["contactos"]
    updated_contact = next((c for c in contacts if c["id"] == contact_id), None)
    assert updated_contact["nombre"] == "Eva"
    assert "555-123-4567" in updated_contact["telefonos"]
    assert "eva.new@example.com" in updated_contact["emails"]

def test_delete_contact(auth_client):
    client, token = auth_client
    headers = {'Authorization': f'Bearer {token}'}

    # Create a contact to delete
    create_response = client.post('/contactos/', headers=headers, json={
        "nombre": "Frank", "telefonos": ["111-111-1111"], "emails": ["frank@example.com"]})
    contact_id = json.loads(create_response.data)["id"] # Assuming the POST returns the ID

    # Delete the contact
    response = client.delete(f'/contactos/{contact_id}', headers=headers)
    assert response.status_code == 200
    assert json.loads(response.data)["message"] == "Contacto eliminado"

    # Verify deletion
    get_response = client.get('/contactos/', headers=headers)
    contacts = json.loads(get_response.data)["contactos"]
    deleted_contact = next((c for c in contacts if c["id"] == contact_id), None)
    assert deleted_contact is None