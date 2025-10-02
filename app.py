from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from dotenv import load_dotenv
import os
from datetime import timedelta
from config import Config

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration
app.config['MONGO_URI'] = Config.MONGO_URI
app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = Config.JWT_ACCESS_TOKEN_EXPIRES

# Initialize extensions
mongo = PyMongo(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
CORS(app)

# Initialize database service
from services.database import db_service
db_service.init_app(app)

# Import routes
from routes.auth_routes import auth_bp
from routes.category_routes import category_bp
from routes.expense_routes import expense_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(category_bp, url_prefix='/api')
app.register_blueprint(expense_bp, url_prefix='/api')

# Register error handlers
from utils.error_handlers import register_error_handlers
register_error_handlers(app)

@app.route('/')
def home():
    return {'message': 'Expense Tracker API is running!', 'status': 'success'}

@app.route('/health')
def health_check():
    return {'status': 'healthy', 'message': 'API is operational'}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
