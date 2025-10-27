import pytest
from app import app # app is still needed for the test functions
import json

def test_register_and_login(client):
    # Test registration
    register_data = {"username": "testuser", "password": "testpassword"}
    response = client.post('/auth/register', json=register_data)
    assert response.status_code == 201
    assert json.loads(response.data)["message"] == "Usuario creado"

    # Test login
    login_data = {"username": "testuser", "password": "testpassword"}
    response = client.post('/auth/login', json=login_data)
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert "access_token" in response_data
    assert "refresh_token" in response_data

    # Test registration with existing username
    response = client.post('/auth/register', json=register_data)
    assert response.status_code == 400
    assert json.loads(response.data)["error"] == "Usuario ya existe"

    # Test login with invalid credentials
    invalid_login_data = {"username": "testuser", "password": "wrongpassword"}
    response = client.post('/auth/login', json=invalid_login_data)
    assert response.status_code == 401
    assert json.loads(response.data)["error"] == "Credenciales inválidas"

def test_logout_and_blacklisted_token(client):
    # Register and login a user
    register_data = {"username": "logoutuser", "password": "logoutpassword"}
    client.post('/auth/register', json=register_data)
    login_data = {"username": "logoutuser", "password": "logoutpassword"}
    response = client.post('/auth/login', json=login_data)
    response_data = json.loads(response.data)
    access_token = response_data["access_token"]
    # refresh_token = response_data["refresh_token"] # Not needed for this test

    headers = {'Authorization': f'Bearer {access_token}'}

    # Logout the user
    logout_response = client.post('/auth/logout', headers=headers)
    assert logout_response.status_code == 200
    assert json.loads(logout_response.data)["message"] == "Sesión cerrada exitosamente"

    # Try to access a protected endpoint with the blacklisted token
    protected_response = client.get('/contactos/', headers=headers)
    assert protected_response.status_code == 401
    assert json.loads(protected_response.data)["error"] == "Token revocado"

def test_refresh_token(client):
    # Register and login a user
    register_data = {"username": "refreshuser", "password": "refreshpassword"}
    client.post('/auth/register', json=register_data)
    login_data = {"username": "refreshuser", "password": "refreshpassword"}
    response = client.post('/auth/login', json=login_data)
    response_data = json.loads(response.data)
    old_access_token = response_data["access_token"]
    old_refresh_token = response_data["refresh_token"]

    # Request a new access token using the refresh token
    refresh_response = client.post('/auth/refresh', json={"refresh_token": old_refresh_token})
    assert refresh_response.status_code == 200
    refresh_response_data = json.loads(refresh_response.data)
    assert "access_token" in refresh_response_data
    assert "refresh_token" in refresh_response_data
    new_access_token = refresh_response_data["access_token"]
    new_refresh_token = refresh_response_data["refresh_token"]

    # Verify new access token works
    headers = {'Authorization': f'Bearer {new_access_token}'}
    protected_response = client.get('/contactos/', headers=headers)
    assert protected_response.status_code == 200 # Should be authorized

    # Verify old refresh token no longer works (due to rotation)
    invalid_refresh_response = client.post('/auth/refresh', json={"refresh_token": old_refresh_token})
    assert invalid_refresh_response.status_code == 401
    assert json.loads(invalid_refresh_response.data)["error"] == "Refresh token inválido"

    # Verify refresh with missing token
    missing_token_response = client.post('/auth/refresh', json={})
    assert missing_token_response.status_code == 401
    assert json.loads(missing_token_response.data)["error"] == "Refresh token ausente"

def test_register_validation(client):
    # Test missing username
    response = client.post('/auth/register', json={"password": "password123"})
    assert response.status_code == 400
    assert "username" in json.loads(response.data)

    # Test missing password
    response = client.post('/auth/register', json={"username": "short"})
    assert response.status_code == 400
    assert "password" in json.loads(response.data)

    # Test username too short (min 4)
    response = client.post('/auth/register', json={"username": "abc", "password": "password123"})
    assert response.status_code == 400
    assert "username" in json.loads(response.data)

    # Test username too long (max 80) - assuming a very long string
    long_username = "a" * 81
    response = client.post('/auth/register', json={"username": long_username, "password": "password123"})
    assert response.status_code == 400
    assert "username" in json.loads(response.data)

    # Test password too short (min 8)
    response = client.post('/auth/register', json={"username": "validuser", "password": "short"})
    assert response.status_code == 400
    assert "password" in json.loads(response.data)

    # Test password too long (max 255) - assuming a very long string
    long_password = "p" * 256
    response = client.post('/auth/register', json={"username": "validuser2", "password": long_password})
    assert response.status_code == 400
    assert "password" in json.loads(response.data)

def test_login_validation(client):
    # Test missing username
    response = client.post('/auth/login', json={"password": "anypassword"})
    assert response.status_code == 400
    assert "username" in json.loads(response.data)

    # Test missing password
    response = client.post('/auth/login', json={"username": "anyuser"})
    assert response.status_code == 400
    assert "password" in json.loads(response.data)

