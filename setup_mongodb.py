#!/usr/bin/env python3
"""
MongoDB Setup Helper for Expense Tracker API
This script helps configure MongoDB connection
"""

import os
from urllib.parse import quote_plus

def setup_local_mongodb():
    """Setup for local MongoDB installation"""
    print("Local MongoDB Setup:")
    print("MONGO_URI=mongodb://localhost:27017/expense_tracker")
    return "mongodb://localhost:27017/expense_tracker"

def setup_mongodb_atlas():
    """Setup for MongoDB Atlas (Cloud)"""
    print("\nMongoDB Atlas Setup:")
    
    username = input("Enter your MongoDB Atlas username: ")
    password = input("Enter your MongoDB Atlas password: ")
    cluster_url = input("Enter your cluster URL (e.g., cluster0.xxxxx.mongodb.net): ")
    
    # URL encode the password to handle special characters
    encoded_password = quote_plus(password)
    
    mongo_uri = f"mongodb+srv://{username}:{encoded_password}@{cluster_url}/expense_tracker?retryWrites=true&w=majority"
    
    print(f"\nYour MongoDB URI:")
    print(f"MONGO_URI={mongo_uri}")
    
    return mongo_uri

def setup_mongodb_with_auth():
    """Setup for local MongoDB with authentication"""
    print("\nLocal MongoDB with Authentication:")
    
    username = input("Enter your MongoDB username: ")
    password = input("Enter your MongoDB password: ")
    host = input("Enter MongoDB host (default: localhost): ") or "localhost"
    port = input("Enter MongoDB port (default: 27017): ") or "27017"
    
    # URL encode the password to handle special characters
    encoded_password = quote_plus(password)
    
    mongo_uri = f"mongodb://{username}:{encoded_password}@{host}:{port}/expense_tracker?authSource=admin"
    
    print(f"\nYour MongoDB URI:")
    print(f"MONGO_URI={mongo_uri}")
    
    return mongo_uri

def create_env_file(mongo_uri):
    """Create .env file with the MongoDB URI"""
    env_content = f"""# Expense Tracker API Environment Variables
MONGO_URI={mongo_uri}
JWT_SECRET_KEY=KdQ8MBny_gA-Rt7pdVTP69wnzxvJxnelYqBx8VaXQBY
FLASK_ENV=development
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print(f"\n✅ Created .env file successfully!")
        print("Your API is now configured to use this MongoDB connection.")
    except Exception as e:
        print(f"\n❌ Could not create .env file: {e}")
        print("You can manually create a .env file with the URI above.")

def main():
    print("MongoDB Setup for Expense Tracker API")
    print("=" * 50)
    
    print("\nChoose your MongoDB setup:")
    print("1. Local MongoDB (no authentication)")
    print("2. Local MongoDB (with authentication)")
    print("3. MongoDB Atlas (Cloud)")
    print("4. Custom URI")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        mongo_uri = setup_local_mongodb()
    elif choice == "2":
        mongo_uri = setup_mongodb_with_auth()
    elif choice == "3":
        mongo_uri = setup_mongodb_atlas()
    elif choice == "4":
        mongo_uri = input("Enter your custom MongoDB URI: ").strip()
    else:
        print("Invalid choice. Using default local MongoDB.")
        mongo_uri = "mongodb://localhost:27017/expense_tracker"
    
    print(f"\n📋 Final MongoDB URI:")
    print(f"{mongo_uri}")
    
    create_env = input("\nCreate .env file with this configuration? (y/n): ").lower().strip()
    if create_env in ['y', 'yes']:
        create_env_file(mongo_uri)
    
    print(f"\n🚀 Next steps:")
    print("1. Make sure MongoDB is running")
    print("2. Run: python app.py")
    print("3. Test with: python test_api.py")
    print("4. API will be available at: http://localhost:5000")

if __name__ == "__main__":
    main()
