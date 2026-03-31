import requests
import json

def test_full_application():
    base_url = "http://localhost:8001"
    
    print("Testing Full AnythingLibrary Application")
    print("=" * 50)
    
    # Test 1: Health Check
    print("\n1. Testing Health Endpoints...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"   [PASS] Root: {response.status_code} - {response.json()['message']}")
        
        response = requests.get(f"{base_url}/health")
        print(f"   [PASS] Health: {response.status_code} - {response.json()['status']}")
        
        response = requests.get(f"{base_url}/providers")
        providers = response.json()['providers']
        print(f"   [PASS] Providers: {response.status_code} - Available: {providers}")
    except Exception as e:
        print(f"   [FAIL] Health check failed: {e}")
        return
    
    # Test 2: Simple Math Question
    print("\n2. Testing Simple Math Question...")
    try:
        test_data = {
            "prompt": "What is 15 + 27? Give just the number.",
            "providers": ["google"],
            "max_tokens": 50,
            "temperature": 0.1
        }
        response = requests.post(f"{base_url}/compare", json=test_data)
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
            print(f"   [FAIL] Request failed: {response.status_code}")
    except Exception as e:
        print(f"   [FAIL] Math test failed: {e}")
    
    # Test 3: Creative Writing
    print("\n3. Testing Creative Writing...")
    try:
        test_data = {
            "prompt": "Write a short haiku about programming.",
            "providers": ["google"],
            "max_tokens": 100,
            "temperature": 0.8
        }
        response = requests.post(f"{base_url}/compare", json=test_data)
        if response.status_code == 200:
            data = response.json()
            for resp in data['responses']:
                provider = resp['provider']
                error = resp.get('error')
                if error:
                    print(f"   [FAIL] {provider}: {error}")
                else:
                    haiku = resp['response'].strip()
                    print(f"   [PASS] {provider}: {haiku[:100]}...")
        else:
            print(f"   [FAIL] Request failed: {response.status_code}")
    except Exception as e:
        print(f"   [FAIL] Creative test failed: {e}")
    
    print("\n" + "=" * 50)
    print("Full Application Test Complete!")
    print("Ready for frontend testing at http://localhost:3000")

if __name__ == "__main__":
    test_full_application()
