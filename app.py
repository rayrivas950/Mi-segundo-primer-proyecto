from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from auth.routes import auth_bp
from contactos.routes import contactos_bp
from extensions import limiter, db, ma
from config import Config
import models

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
limiter.init_app(app)
db.init_app(app)
ma.init_app(app)
migrate = Migrate(app, db)
CORS(app) # Enable CORS for all routes

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(contactos_bp)

if __name__ == '__main__':
    app.run(debug=True)
