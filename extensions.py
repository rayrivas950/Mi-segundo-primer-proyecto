from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

limiter = Limiter(
    get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="redis://localhost:6379",
    strategy="fixed-window"
)

# Conditionally disable limiter if app is in testing mode
@limiter.exempt
def exempt_if_testing():
    return current_app.config.get("TESTING", False)

limiter.request_filter(exempt_if_testing)

db = SQLAlchemy()
ma = Marshmallow()

# JWT Blacklist (in-memory for simplicity, use Redis in production)
revoked_tokens = set()

def add_token_to_blacklist(token):
    revoked_tokens.add(token)

def is_token_blacklisted(token):
    return token in revoked_tokens