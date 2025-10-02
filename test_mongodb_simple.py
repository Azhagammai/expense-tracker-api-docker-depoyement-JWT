#!/usr/bin/env python3
"""
Test MongoDB connection with different authentication methods
"""

from pymongo import MongoClient
from datetime import datetime

def test_mongodb_connections():
    print("Testing MongoDB connections...")
    print("=" * 50)
    
    # Test different connection strings
    connection_strings = [
        # No authentication
        'mongodb://localhost:27017/expense_tracker',
        # With your credentials
        'mongodb://admin:Azhagammai%4025879865@localhost:27017/expense_tracker?authSource=admin',
        # Alternative format
        'mongodb://admin:Azhagammai%4025879865@localhost:27017/expense_tracker',
        # With different auth source
        'mongodb://admin:Azhagammai%4025879865@localhost:27017/expense_tracker?authSource=expense_tracker'
    ]
    
    for i, mongo_uri in enumerate(connection_strings, 1):
        print(f"\nTest {i}: {mongo_uri}")
        try:
            client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
            
            # Test connection
            client.admin.command('ping')
            print("SUCCESS: Connection established")
            
            # Test database access
            db = client['expense_tracker']
            collections = db.list_collection_names()
            print(f"SUCCESS: Database accessible, collections: {collections}")
            
            # Test insert
            test_doc = {'test': True, 'timestamp': datetime.utcnow()}
            result = db.users.insert_one(test_doc)
            print(f"SUCCESS: Insert test (ID: {result.inserted_id})")
            
            # Clean up
            db.users.delete_one({'_id': result.inserted_id})
            print("SUCCESS: Cleanup completed")
            
            client.close()
            print(f"WORKING CONNECTION STRING: {mongo_uri}")
            return mongo_uri
            
        except Exception as e:
            print(f"FAILED: {str(e)}")
            try:
                client.close()
            except:
                pass
    
    print("\nAll connection attempts failed.")
    print("Please check:")
    print("1. MongoDB is running")
    print("2. Authentication credentials")
    print("3. MongoDB configuration")
    return None

if __name__ == "__main__":
    working_uri = test_mongodb_connections()
    if working_uri:
        print(f"\nUse this connection string: {working_uri}")
    else:
        print("\nNo working connection found.")
