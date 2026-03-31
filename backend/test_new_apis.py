import requests
import json

def test_new_api_integrations():
    base_url = "http://localhost:8001"
    
    print("Testing New API Integrations")
    print("=" * 40)
    
    # Test 1: Check available providers
    print("\n1. Testing available providers...")
    try:
        response = requests.get(f"{base_url}/providers")
        if response.status_code == 200:
            providers = response.json()['providers']
            print(f"   Available providers: {providers}")
        else:
            print(f"   Error: {response.status_code}")
            return
    except Exception as e:
        print(f"   Exception: {e}")
        return
    
    # Test 2: Test Cohere API
    print("\n2. Testing Cohere API...")
    try:
        test_data = {
            "prompt": "What is 7 + 8? Give just the number.",
            "providers": ["cohere"],
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
        print(f"   [FAIL] Exception: {e}")
    
    # Test 3: Test Grok API
    print("\n3. Testing Grok API...")
    try:
        test_data = {
            "prompt": "What is 9 + 6? Give just the number.",
            "providers": ["grok"],
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
        print(f"   [FAIL] Exception: {e}")
    
    # Test 4: Test all available providers together
    print("\n4. Testing all available providers...")
    try:
        test_data = {
            "prompt": "What is AI? Give a short definition.",
            "providers": providers,
            "max_tokens": 100,
            "temperature": 0.7
        }
        response = requests.post(f"{base_url}/compare", json=test_data)
        if response.status_code == 200:
            data = response.json()
            print(f"   Received {len(data['responses'])} responses:")
            for resp in data['responses']:
                provider = resp['provider']
                error = resp.get('error')
                if error:
                    print(f"   [FAIL] {provider}: {error}")
                else:
                    answer = resp['response'].strip()[:100]
                    print(f"   [PASS] {provider}: {answer}...")
        else:
            print(f"   [FAIL] Request failed: {response.status_code}")
    except Exception as e:
        print(f"   [FAIL] Exception: {e}")
    
    print("\n" + "=" * 40)
    print("New API integration test complete!")

if __name__ == "__main__":
    test_new_api_integrations()
