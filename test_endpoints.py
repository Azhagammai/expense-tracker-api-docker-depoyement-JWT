import requests
import json

def test_api():
    base_url = "http://127.0.0.1:5000"
    
    print("Testing API endpoints...")
    print("=" * 50)
    
    # Test 1: Home endpoint
    try:
        print("1. Testing home endpoint (/)...")
        response = requests.get(f"{base_url}/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test 2: Health endpoint
    try:
        print("2. Testing health endpoint (/health)...")
        response = requests.get(f"{base_url}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test 3: API info endpoint
    try:
        print("3. Testing API info endpoint (/api/info)...")
        response = requests.get(f"{base_url}/api/info")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test 4: User registration (this should work)
    try:
        print("4. Testing user registration...")
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123"
        }
        response = requests.post(f"{base_url}/api/auth/register", json=user_data)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    test_api()
