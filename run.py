#!/usr/bin/env python3
"""
Startup script for the Expense Tracker API
This script provides different ways to run the application
"""

import os
import sys
import argparse
from app import app

def run_development():
    """Run the application in development mode"""
    print("🚀 Starting Expense Tracker API in development mode...")
    print("📍 Server will be available at: http://localhost:5000")
    print("📖 API documentation available in README.md")
    print("🧪 Run test_api.py to test the endpoints")
    print("-" * 50)
    
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )

def run_production():
    """Run the application in production mode"""
    print("🚀 Starting Expense Tracker API in production mode...")
    
    app.run(
        debug=False,
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000))
    )

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import flask
        import flask_pymongo
        import flask_jwt_extended
        import flask_bcrypt
        import flask_cors
        import pymongo
        import marshmallow
        import python_dateutil
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("📦 Please run: pip install -r requirements.txt")
        return False

def check_mongodb_connection():
    """Check if MongoDB is accessible"""
    try:
        from services.database import db_service
        with app.app_context():
            db_service.init_app(app)
            # Try to get database info
            db_service.get_db().command('ping')
        print("✅ MongoDB connection successful")
        return True
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        print("🔧 Please ensure MongoDB is running and accessible")
        return False

def main():
    parser = argparse.ArgumentParser(description='Expense Tracker API Runner')
    parser.add_argument('--mode', choices=['dev', 'prod', 'check'], default='dev',
                      help='Run mode: dev (development), prod (production), check (dependencies)')
    
    args = parser.parse_args()
    
    print("Expense Tracker API")
    print("=" * 50)
    
    if args.mode == 'check':
        print("🔍 Checking system dependencies...")
        deps_ok = check_dependencies()
        mongo_ok = check_mongodb_connection()
        
        if deps_ok and mongo_ok:
            print("\n🎉 All checks passed! You're ready to run the API.")
        else:
            print("\n⚠️  Please fix the issues above before running the API.")
            sys.exit(1)
    
    elif args.mode == 'dev':
        if not check_dependencies():
            sys.exit(1)
        run_development()
    
    elif args.mode == 'prod':
        if not check_dependencies():
            sys.exit(1)
        run_production()

if __name__ == '__main__':
    main()
