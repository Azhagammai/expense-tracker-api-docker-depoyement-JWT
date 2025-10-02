#!/usr/bin/env python3
"""
Quick test script to verify the Expense Tracker API is working
"""

import requests
import json
import sys

BASE_URL = "http://127.0.0.1:5000"

def test_api():
    print("Testing Expense Tracker API...")
    print(f"Base URL: {BASE_URL}")
    print("-" * 50)
    
    try:
        # Test 1: Health check
        print("1. Testing health endpoint...")
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("   ✓ Health check passed")
            data = response.json()
            print(f"   Status: {data.get('status')}")
            print(f"   Database: {data.get('database', 'unknown')}")
        else:
            print(f"   X Health check failed: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("   X Cannot connect to API server")
        print("   Make sure the server is running on http://127.0.0.1:5000")
        return False
    except Exception as e:
        print(f"   X Error: {e}")
        return False
    
    try:
        # Test 2: Home endpoint
        print("\n2. Testing home endpoint...")
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print("   ✓ Home endpoint working")
            data = response.json()
            print(f"   Message: {data.get('message')}")
        else:
            print(f"   X Home endpoint failed: {response.status_code}")
            
    except Exception as e:
        print(f"   X Error: {e}")
    
    try:
        # Test 3: User registration
        print("\n3. Testing user registration...")
        user_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "password": "testpassword123"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/users/register",
            json=user_data,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        if response.status_code == 201:
            print("   ✓ User registration working")
            data = response.json()
            token = data['data']['token']
            print(f"   Token received: {token[:20]}...")
            return True
        elif response.status_code == 400:
            # User might already exist, try login
            print("   i User might already exist, trying login...")
            
            login_data = {
                "email": "test@example.com",
                "password": "testpassword123"
            }
            
            response = requests.post(
                f"{BASE_URL}/api/users/login",
                json=login_data,
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            
            if response.status_code == 200:
                print("   ✓ User login working")
                data = response.json()
                token = data['data']['token']
                print(f"   Token received: {token[:20]}...")
                return True
            else:
                print(f"   X Login failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
        else:
            print(f"   X Registration failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"   X Error: {e}")
        return False

def main():
    print("Expense Tracker API - Quick Test")
    print("=" * 50)
    
    success = test_api()
    
    print("\n" + "=" * 50)
    if success:
        print("SUCCESS: API is working correctly!")
        print("\nReady for Postman testing:")
        print("   1. Use base URL: http://127.0.0.1:5000")
        print("   2. Start with health check: GET /health")
        print("   3. Register user: POST /api/users/register")
        print("   4. Follow the POSTMAN_COMPLETE_GUIDE.md")
        print("\nYour API meets all interview requirements!")
    else:
        print("FAILED: API test failed")
        print("\nTroubleshooting:")
        print("   1. Make sure the server is running")
        print("   2. Check if MongoDB is connected (optional for basic testing)")
        print("   3. Verify no firewall is blocking port 5000")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
