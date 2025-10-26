from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import current_app

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