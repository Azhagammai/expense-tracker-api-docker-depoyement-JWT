#!/usr/bin/env python3
"""
Test the MongoDB-connected API to verify data persistence
"""

import requests
import json
import time

def test_mongodb_api():
    base_url = "http://127.0.0.1:5000"
    
    print("Testing MongoDB-Connected API...")
    print("=" * 60)
    
    # Test 1: Health check
    try:
        print("1. Testing health endpoint...")
        response = requests.get(f"{base_url}/health")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Database: {data.get('database', 'Unknown')}")
            print(f"   Users: {data.get('data_counts', {}).get('users', 0)}")
            print(f"   Categories: {data.get('data_counts', {}).get('categories', 0)}")
            print(f"   Expenses: {data.get('data_counts', {}).get('expenses', 0)}")
        else:
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test 2: User registration
    try:
        print("2. Testing user registration...")
        user_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "password": "testpass123"
        }
        response = requests.post(f"{base_url}/api/users/register", json=user_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            data = response.json()
            print(f"   User ID: {data['data']['user']['id']}")
            print(f"   Token: {data['data']['token'][:50]}...")
            token = data['data']['token']
        else:
            print(f"   Response: {response.text}")
            token = None
    except Exception as e:
        print(f"   Error: {e}")
        token = None
    
    print()
    
    # Test 3: User login
    if token:
        try:
            print("3. Testing user login...")
            login_data = {
                "email": "test@example.com",
                "password": "testpass123"
            }
            response = requests.post(f"{base_url}/api/users/login", json=login_data)
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print("   Login successful")
            else:
                print(f"   Response: {response.text}")
        except Exception as e:
            print(f"   Error: {e}")
    
    print()
    
    # Test 4: Create category (requires authentication)
    if token:
        try:
            print("4. Testing category creation...")
            headers = {'Authorization': f'Bearer {token}'}
            category_data = {
                "title": "Groceries",
                "description": "Food and household items"
            }
            response = requests.post(f"{base_url}/api/categories", json=category_data, headers=headers)
            print(f"   Status: {response.status_code}")
            if response.status_code == 201:
                data = response.json()
                print(f"   Category ID: {data['data']['category']['id']}")
                category_id = data['data']['category']['id']
            else:
                print(f"   Response: {response.text}")
                category_id = None
        except Exception as e:
            print(f"   Error: {e}")
            category_id = None
    else:
        category_id = None
    
    print()
    
    # Test 5: Create expense (requires authentication)
    if token and category_id:
        try:
            print("5. Testing expense creation...")
            headers = {'Authorization': f'Bearer {token}'}
            expense_data = {
                "amount": 25.50,
                "note": "Grocery shopping",
                "expense_date": "2025-10-02T10:00:00Z",
                "category_id": category_id
            }
            response = requests.post(f"{base_url}/api/expenses", json=expense_data, headers=headers)
            print(f"   Status: {response.status_code}")
            if response.status_code == 201:
                data = response.json()
                print(f"   Expense ID: {data['data']['expense']['id']}")
                print(f"   Amount: ${data['data']['expense']['amount']}")
            else:
                print(f"   Response: {response.text}")
        except Exception as e:
            print(f"   Error: {e}")
    
    print()
    
    # Test 6: Get expenses
    if token:
        try:
            print("6. Testing expense retrieval...")
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.get(f"{base_url}/api/expenses", headers=headers)
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                expenses = data['data']['expenses']
                print(f"   Found {len(expenses)} expenses")
                for expense in expenses:
                    print(f"   - ${expense['amount']}: {expense['note']}")
            else:
                print(f"   Response: {response.text}")
        except Exception as e:
            print(f"   Error: {e}")
    
    print()
    
    # Test 7: Final health check to verify data persistence
    try:
        print("7. Final health check...")
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"   Final counts:")
            print(f"   Users: {data.get('data_counts', {}).get('users', 0)}")
            print(f"   Categories: {data.get('data_counts', {}).get('categories', 0)}")
            print(f"   Expenses: {data.get('data_counts', {}).get('expenses', 0)}")
            
            if data.get('data_counts', {}).get('users', 0) > 0:
                print("SUCCESS: Data is being stored in MongoDB!")
            else:
                print("WARNING: No data found in MongoDB")
        else:
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    test_mongodb_api()
