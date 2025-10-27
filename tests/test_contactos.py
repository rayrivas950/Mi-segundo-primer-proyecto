import pytest
from app import app # app is still needed for the test functions
import json

# Fixtures client and auth_client are now in conftest.py

def test_create_contact(auth_client):
    client, access_token = auth_client
    headers = {'Authorization': f'Bearer {access_token}'}
    # Updated contact_data format for Marshmallow schema
    contact_data = {
        "nombre": "Alice",
        "telefonos": [{"telefono": "111-222-3333"}],
        "emails": [{"email": "alice@example.com"}]
    }
    response = client.post('/contactos/', headers=headers, json=contact_data)
    assert response.status_code == 201
    response_data = json.loads(response.data)
    assert response_data["nombre"] == "Alice"
    assert response_data["telefonos"][0]["telefono"] == "111-222-3333"
    assert response_data["emails"][0]["email"] == "alice@example.com"
    assert "id" in response_data # Ensure ID is returned

def test_create_contact_unauthorized(client):
    contact_data = {
        "nombre": "Alice",
        "telefonos": [{"telefono": "111-222-3333"}],
        "emails": [{"email": "alice@example.com"}]
    }
    response = client.post('/contactos/', json=contact_data)
    assert response.status_code == 401
    assert json.loads(response.data)["error"] == "Token inválido o ausente"

def test_get_contacts(auth_client):
    client, access_token = auth_client
    headers = {'Authorization': f'Bearer {access_token}'}

    # Create a contact first
    contact_data = {
        "nombre": "Bob",
        "telefonos": [{"telefono": "444-555-6666"}],
        "emails": [{"email": "bob@example.com"}]
    }
    client.post('/contactos/', headers=headers, json=contact_data)

    response = client.get('/contactos/', headers=headers)
    assert response.status_code == 200
    contacts = json.loads(response.data) # API now returns a list directly
    assert len(contacts) == 1
    assert contacts[0]["nombre"] == "Bob"

def test_search_contacts(auth_client):
    client, access_token = auth_client
    headers = {'Authorization': f'Bearer {access_token}'}

    # Create contacts for searching
    client.post('/contactos/', headers=headers, json={
        "nombre": "Charlie", "telefonos": [{"telefono": "123-456-7890"}], "emails": [{"email": "charlie@example.com"}]})
    client.post('/contactos/', headers=headers, json={
        "nombre": "David", "telefonos": [{"telefono": "987-654-3210"}], "emails": [{"email": "david@test.com"}]})

    # Search by name
    response = client.get('/contactos/?search=Charlie', headers=headers)
    assert response.status_code == 200
    contacts = json.loads(response.data) # API now returns a list directly
    assert len(contacts) == 1
    assert contacts[0]["nombre"] == "Charlie"

    # Search by phone
    response = client.get('/contactos/?search=987', headers=headers)
    assert response.status_code == 200
    contacts = json.loads(response.data) # API now returns a list directly
    assert len(contacts) == 1
    assert contacts[0]["nombre"] == "David"

    # Search by email
    response = client.get('/contactos/?search=charlie@example.com', headers=headers)
    assert response.status_code == 200
    contacts = json.loads(response.data) # API now returns a list directly
    assert len(contacts) == 1
    assert contacts[0]["nombre"] == "Charlie"

def test_update_contact(auth_client):
    client, access_token = auth_client
    headers = {'Authorization': f'Bearer {access_token}'}

    # Create a contact to update
    create_response = client.post('/contactos/', headers=headers, json={
        "nombre": "Eve", "telefonos": [{"telefono": "111-222-3333"}], "emails": [{"email": "eve@example.com"}]})
    create_response_data = json.loads(create_response.data)
    contact_id = create_response_data["id"] # Extract ID directly from serialized object

    # Update the contact
    update_data = {
        "nombre": "Eva",
        "telefonos": [{"telefono": "555-123-4567"}],
        "emails": [{"email": "eva.new@example.com"}]
    }
    response = client.put(f'/contactos/{contact_id}', headers=headers, json=update_data)
    assert response.status_code == 200
    updated_contact_data = json.loads(response.data) # API now returns the updated serialized contact
    assert updated_contact_data["nombre"] == "Eva"
    assert updated_contact_data["telefonos"][0]["telefono"] == "555-123-4567"
    assert updated_contact_data["emails"][0]["email"] == "eva.new@example.com"


    # Verify the update by getting all contacts and finding the updated one
    get_response = client.get('/contactos/', headers=headers)
    contacts = json.loads(get_response.data) # API now returns a list directly
    updated_contact = next((c for c in contacts if c["id"] == contact_id), None)
    assert updated_contact["nombre"] == "Eva"
    assert updated_contact["telefonos"][0]["telefono"] == "555-123-4567"
    assert updated_contact["emails"][0]["email"] == "eva.new@example.com"

def test_delete_contact(auth_client):
    client, access_token = auth_client
    headers = {'Authorization': f'Bearer {access_token}'}

    # Create a contact to delete
    create_response = client.post('/contactos/', headers=headers, json={
        "nombre": "Frank", "telefonos": [{"telefono": "111-111-1111"}], "emails": [{"email": "frank@example.com"}]})
    create_response_data = json.loads(create_response.data)
    contact_id = create_response_data["id"] # Extract ID directly from serialized object

    # Delete the contact
    response = client.delete(f'/contactos/{contact_id}', headers=headers)
    assert response.status_code == 200
    assert json.loads(response.data)["message"] == "Contacto eliminado"

    # Verify deletion
    get_response = client.get('/contactos/', headers=headers)
    contacts = json.loads(get_response.data) # API now returns a list directly
    deleted_contact = next((c for c in contacts if c["id"] == contact_id), None)
    assert deleted_contact is None