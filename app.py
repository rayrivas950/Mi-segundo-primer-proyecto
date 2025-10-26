from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from db import create_tables, close_db_connection
from auth.routes import auth_bp
from contactos.routes import contactos_bp
from extensions import limiter

app = Flask(__name__)

limiter.init_app(app)

with app.app_context():
    create_tables()
app.register_blueprint(auth_bp)
app.register_blueprint(contactos_bp)
app.teardown_appcontext(close_db_connection)

if __name__ == '__main__':
    app.run(debug=True)
