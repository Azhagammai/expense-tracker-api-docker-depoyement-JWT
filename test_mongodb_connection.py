#!/usr/bin/env python3
"""
Test MongoDB connection with your credentials
"""

from pymongo import MongoClient
from datetime import datetime

def test_mongodb_connection():
    print("Testing MongoDB connection...")
    print("=" * 50)
    
    # Your MongoDB connection string
    MONGO_URI = 'mongodb://admin:Azhagammai%4025879865@localhost:27017/expense_tracker?authSource=admin'
    
    try:
        # Test connection
        client = MongoClient(MONGO_URI)
        
        # Test database access
        db = client['expense_tracker']
        
        # Test collection access
        users_collection = db['users']
        categories_collection = db['categories']
        expenses_collection = db['expenses']
        
        print("SUCCESS: MongoDB Connection")
        print(f"   Database: {db.name}")
        print(f"   Collections: users, categories, expenses")
        
        # Test insert/read
        test_doc = {
            'test': True,
            'timestamp': datetime.utcnow(),
            'message': 'Connection test successful'
        }
        
        # Insert test document
        result = users_collection.insert_one(test_doc)
        print(f"SUCCESS: Test Insert (ID: {result.inserted_id})")
        
        # Read test document
        found_doc = users_collection.find_one({'_id': result.inserted_id})
        if found_doc:
            print("SUCCESS: Test Read")
        else:
            print("FAILED: Test Read")
        
        # Clean up test document
        users_collection.delete_one({'_id': result.inserted_id})
        print("SUCCESS: Test Cleanup")
        
        # Show current data counts
        users_count = users_collection.count_documents({})
        categories_count = categories_collection.count_documents({})
        expenses_count = expenses_collection.count_documents({})
        
        print("\nCurrent Data Counts:")
        print(f"   Users: {users_count}")
        print(f"   Categories: {categories_count}")
        print(f"   Expenses: {expenses_count}")
        
        print("\nMongoDB is ready for the API!")
        return True
        
    except Exception as e:
        print(f"FAILED: MongoDB Connection")
        print(f"   Error: {str(e)}")
        print("\nTroubleshooting:")
        print("   1. Make sure MongoDB is running on your system")
        print("   2. Check if the username/password is correct")
        print("   3. Verify MongoDB is accessible on localhost:27017")
        print("   4. Check if authentication is required")
        return False
    
    finally:
        try:
            client.close()
        except:
            pass

if __name__ == "__main__":
    test_mongodb_connection()
