#!/usr/bin/env python3
"""
Simple test to check if all components work
"""

print("Testing Expense Tracker API Components...")

# Test 1: Import all modules
try:
    from flask import Flask
    from flask_pymongo import PyMongo
    from flask_jwt_extended import JWTManager
    from flask_bcrypt import Bcrypt
    from flask_cors import CORS
    print("✓ All Flask modules imported successfully")
except ImportError as e:
    print(f"X Import error: {e}")
    exit(1)

# Test 2: Create basic Flask app
try:
    app = Flask(__name__)
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/expense_tracker'
    app.config['JWT_SECRET_KEY'] = 'test_key'
    print("✓ Flask app created successfully")
except Exception as e:
    print(f"X Flask app creation error: {e}")
    exit(1)

# Test 3: Initialize extensions
try:
    mongo = PyMongo(app)
    jwt = JWTManager(app)
    bcrypt = Bcrypt(app)
    CORS(app)
    print("✓ Flask extensions initialized successfully")
except Exception as e:
    print(f"X Extension initialization error: {e}")
    print("Note: This might be due to MongoDB not running")

# Test 4: Test MongoDB connection
try:
    with app.app_context():
        # Try to ping MongoDB
        mongo.db.command('ping')
        print("✓ MongoDB connection successful")
except Exception as e:
    print(f"! MongoDB connection failed: {e}")
    print("   This is expected if MongoDB is not running")

# Test 5: Create a simple route and test
@app.route('/test')
def test_route():
    return {'status': 'success', 'message': 'API is working!'}

@app.route('/health')
def health():
    return {'status': 'healthy', 'message': 'API is operational'}

print("✓ Routes created successfully")

# Test 6: Start server
print("\nStarting test server on http://localhost:5001...")
print("Test URLs:")
print("   - http://localhost:5001/test")
print("   - http://localhost:5001/health")
print("\nPress Ctrl+C to stop the server")

if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0', port=5001)
    except Exception as e:
        print(f"X Server startup error: {e}")
