import requests
import json

def test_login():
    base_url = "http://localhost:8001"
    
    print("Testing Login Endpoint")
    print("=" * 30)
    
    # Test 1: Valid login
    print("\n1. Testing valid login...")
    try:
        login_data = {
            "username": "testuser",
            "password": "pass123"
        }
        response = requests.post(f"{base_url}/login", json=login_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Success: {data['message']}")
            print(f"   User: {data['user']['username']}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Exception: {e}")
    
    # Test 2: Invalid login (too short)
    print("\n2. Testing invalid login (short credentials)...")
    try:
        login_data = {
            "username": "ab",
            "password": "123"
        }
        response = requests.post(f"{base_url}/login", json=login_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 401:
            data = response.json()
            print(f"   Expected error: {data['error']}")
        else:
            print(f"   Unexpected: {response.text}")
    except Exception as e:
        print(f"   Exception: {e}")
    
    # Test 3: Missing credentials
    print("\n3. Testing missing credentials...")
    try:
        login_data = {
            "username": "",
            "password": ""
        }
        response = requests.post(f"{base_url}/login", json=login_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 400:
            data = response.json()
            print(f"   Expected error: {data['error']}")
        else:
            print(f"   Unexpected: {response.text}")
    except Exception as e:
        print(f"   Exception: {e}")
    
    print("\n" + "=" * 30)
    print("Login endpoint test complete!")

if __name__ == "__main__":
    test_login()
