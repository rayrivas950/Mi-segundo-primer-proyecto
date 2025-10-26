import pytest
from app import app
from db import create_tables, get_db_connection
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.app_context():
        # Ensure tables are created for testing
        create_tables()
        # Clear users table before each test
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM users")
        conn.commit()
        cur.close()
    with app.test_client() as client:
        yield client

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
    assert "token" in json.loads(response.data)

    # Test registration with existing username
    response = client.post('/auth/register', json=register_data)
    assert response.status_code == 400
    assert json.loads(response.data)["error"] == "Usuario ya existe"

    # Test login with invalid credentials
    invalid_login_data = {"username": "testuser", "password": "wrongpassword"}
    response = client.post('/auth/login', json=invalid_login_data)
    assert response.status_code == 401
    assert json.loads(response.data)["error"] == "Credenciales inválidas"
