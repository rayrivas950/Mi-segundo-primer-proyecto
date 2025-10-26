import os

class Config:
    # It is crucial to use a strong, randomly generated SECRET_KEY in production.
    # Consider a key rotation strategy for enhanced security.
    SECRET_KEY = os.getenv("SECRET_KEY")
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
