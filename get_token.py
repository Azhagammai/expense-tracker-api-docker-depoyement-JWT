#!/usr/bin/env python3
"""
Get JWT token for testing
"""

import requests
import json

def get_token():
    print("Getting JWT token for testing...")
    print("=" * 50)
    
    # Try to register a new user
    try:
        print("1. Trying to register new user...")
        user_data = {
            "first_name": "Test",
            "last_name": "User", 
            "email": "testuser@example.com",
            "password": "testpass123"
        }
        
        response = requests.post("http://127.0.0.1:5000/api/users/register", json=user_data)
        
        if response.status_code == 201:
            data = response.json()
            token = data['data']['token']
            print(f"SUCCESS: User registered!")
            print(f"Token: {token}")
            return token
        elif response.status_code == 400 and "already exists" in response.text:
            print("User already exists, trying login...")
            
            # Try login
            login_data = {
                "email": "testuser@example.com",
                "password": "testpass123"
            }
            
            response = requests.post("http://127.0.0.1:5000/api/users/login", json=login_data)
            
            if response.status_code == 200:
                data = response.json()
                token = data['data']['token']
                print(f"SUCCESS: User logged in!")
                print(f"Token: {token}")
                return token
            else:
                print(f"Login failed: {response.status_code}")
                print(f"Response: {response.text}")
                return None
        else:
            print(f"Registration failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_with_token(token):
    if not token:
        print("No token available for testing")
        return
        
    print("\n2. Testing with token...")
    print("=" * 50)
    
    # Test creating category with token
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        
        category_data = {
            "title": "Leisure",
            "description": "Entertainment and recreation"
        }
        
        response = requests.post("http://127.0.0.1:5000/api/categories", json=category_data, headers=headers)
        
        print(f"Category creation status: {response.status_code}")
        if response.status_code == 201:
            print("SUCCESS: Category created!")
            data = response.json()
            print(f"Category ID: {data['data']['category']['id']}")
        else:
            print(f"Failed: {response.text}")
            
    except Exception as e:
        print(f"Error testing with token: {e}")

if __name__ == "__main__":
    token = get_token()
    test_with_token(token)
    
    if token:
        print(f"\nUse this token in Postman:")
        print(f"Authorization: Bearer {token}")
    else:
        print("\nFailed to get token. Check if API is running.")
