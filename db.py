import psycopg2
from flask import g
from config import Config

def get_db_connection():
    if 'db_conn' not in g:
        g.db_conn = psycopg2.connect(
            host=Config.DB_HOST,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASS
        )
    return g.db_conn

def close_db_connection(exception=None):
    db = g.pop('db_conn', None)
    if db:
        db.close()

def create_tables():
    conn = get_db_connection()
    cur = conn.cursor()

    commands = (
        "CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, username VARCHAR(80) UNIQUE NOT NULL, password VARCHAR(255) NOT NULL, created_at TIMESTAMP DEFAULT NOW());",
        "CREATE TABLE IF NOT EXISTS contactos (id SERIAL PRIMARY KEY, user_id INTEGER NOT NULL, nombre VARCHAR(255) NOT NULL, created_at TIMESTAMP DEFAULT NOW(), FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE);",
        "CREATE TABLE IF NOT EXISTS telefonos (id SERIAL PRIMARY KEY, contacto_id INTEGER NOT NULL, telefono VARCHAR(255) NOT NULL, FOREIGN KEY (contacto_id) REFERENCES contactos(id) ON DELETE CASCADE);",
        "CREATE TABLE IF NOT EXISTS emails (id SERIAL PRIMARY KEY, contacto_id INTEGER NOT NULL, email VARCHAR(255) NOT NULL, FOREIGN KEY (contacto_id) REFERENCES contactos(id) ON DELETE CASCADE);"
    )

    for c in commands:
        cur.execute(c)

    conn.commit()
    cur.close()
