import pytest
from app import app
from extensions import db, revoked_tokens
import json

@pytest.fixture
def client():
    # Use an in-memory SQLite database for testing
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SECRET_KEY'] = 'test_secret_key' # Set a secret key for testing

    with app.app_context():
        db.create_all()
        revoked_tokens.clear() # Clear the blacklist before each test
        yield app.test_client()
        db.session.remove()
        db.drop_all()

@pytest.fixture
def auth_client(client):
    # Register a user
    register_data = {"username": "testuser", "password": "testpassword"}
    client.post('/auth/register', json=register_data)

    # Log in and get token
    login_data = {"username": "testuser", "password": "testpassword"}
    response = client.post('/auth/login', json=login_data)
    response_data = json.loads(response.data)
    access_token = response_data["access_token"]

    return client, access_token
