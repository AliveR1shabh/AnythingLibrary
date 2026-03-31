import requests
import json

def test_full_authentication_flow():
    base_url = "http://localhost:8001"
    
    print("Testing Full Authentication Flow")
    print("=" * 40)
    
    # Step 1: Test login
    print("\n1. Testing user login...")
    try:
        login_data = {
            "username": "demo",
            "password": "test123"
        }
        response = requests.post(f"{base_url}/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            print(f"   [PASS] Login successful: {data['user']['username']}")
            user_token = data['user']
        else:
            print(f"   [FAIL] Login failed: {response.text}")
            return
    except Exception as e:
        print(f"   [FAIL] Login exception: {e}")
        return
    
    # Step 2: Test providers endpoint (should work after login)
    print("\n2. Testing providers endpoint...")
    try:
        response = requests.get(f"{base_url}/providers")
        if response.status_code == 200:
            providers = response.json()['providers']
            print(f"   [PASS] Providers available: {providers}")
        else:
            print(f"   [FAIL] Providers failed: {response.text}")
    except Exception as e:
        print(f"   [FAIL] Providers exception: {e}")
    
    # Step 3: Test AI comparison (should work after login)
    print("\n3. Testing AI comparison...")
    try:
        compare_data = {
            "prompt": "What is 5 + 3?",
            "providers": ["google"],
            "max_tokens": 50,
            "temperature": 0.1
        }
        response = requests.post(f"{base_url}/compare", json=compare_data)
        if response.status_code == 200:
            data = response.json()
            for resp in data['responses']:
                provider = resp['provider']
                error = resp.get('error')
                if error:
                    print(f"   [FAIL] {provider}: {error}")
                else:
                    answer = resp['response'].strip()
                    print(f"   [PASS] {provider}: {answer}")
        else:
            print(f"   [FAIL] Compare failed: {response.text}")
    except Exception as e:
        print(f"   [FAIL] Compare exception: {e}")
    
    print("\n" + "=" * 40)
    print("Full authentication flow test complete!")
    print("✅ Ready for frontend testing at http://localhost:3000")
    print("🔑 Login with: username (3+ chars, alphanumeric) + password (4+ chars)")

if __name__ == "__main__":
    test_full_authentication_flow()
