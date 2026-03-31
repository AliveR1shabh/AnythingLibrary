import requests
import json

def test_new_apis():
    base_url = "http://localhost:8001"
    
    print("Testing New GROQ and Cerebras API Integrations")
    print("=" * 50)
    
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
    
    # Test 2: Test GROQ API
    print("\n2. Testing GROQ API...")
    try:
        test_data = {
            "prompt": "What is artificial intelligence? Provide a detailed explanation in at least 3 lines.",
            "providers": ["groq"],
            "max_tokens": 1000,
            "temperature": 0.7
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
                    lines = answer.split('\n')
                    print(f"   [PASS] {provider}: {len(lines)} lines")
                    print(f"   Response: {answer[:200]}...")
        else:
            print(f"   [FAIL] Request failed: {response.status_code}")
    except Exception as e:
        print(f"   [FAIL] Exception: {e}")
    
    # Test 3: Test Cerebras API
    print("\n3. Testing Cerebras API...")
    try:
        test_data = {
            "prompt": "Explain machine learning in detail. Provide at least 3 lines of explanation.",
            "providers": ["cerebras"],
            "max_tokens": 1000,
            "temperature": 0.7
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
                    lines = answer.split('\n')
                    print(f"   [PASS] {provider}: {len(lines)} lines")
                    print(f"   Response: {answer[:200]}...")
        else:
            print(f"   [FAIL] Request failed: {response.status_code}")
    except Exception as e:
        print(f"   [FAIL] Exception: {e}")
    
    # Test 4: Test all available providers together
    print("\n4. Testing all available providers together...")
    try:
        test_data = {
            "prompt": "What is the future of AI? Provide a comprehensive answer with multiple lines.",
            "providers": providers,
            "max_tokens": 1000,
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
                    answer = resp['response'].strip()
                    lines = answer.split('\n')
                    print(f"   [PASS] {provider}: {len(lines)} lines, {len(answer)} chars")
        else:
            print(f"   [FAIL] Request failed: {response.status_code}")
    except Exception as e:
        print(f"   [FAIL] Exception: {e}")
    
    print("\n" + "=" * 50)
    print("New API integration test complete!")

if __name__ == "__main__":
    test_new_apis()
