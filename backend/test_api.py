import requests
import json

def test_api():
    base_url = "http://localhost:8000"
    
    print("Testing API endpoints...")
    
    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/")
        print(f"Root endpoint: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Root endpoint error: {e}")
    
    # Test providers endpoint
    try:
        response = requests.get(f"{base_url}/providers")
        print(f"Providers endpoint: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Providers endpoint error: {e}")
    
    # Test compare endpoint
    try:
        test_data = {
            "prompt": "What is 2+2?",
            "providers": ["openai", "google"],
            "max_tokens": 100,
            "temperature": 0.7
        }
        response = requests.post(f"{base_url}/compare", json=test_data)
        print(f"Compare endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response has {len(data.get('responses', []))} results")
            for resp in data.get('responses', []):
                provider = resp.get('provider', 'Unknown')
                error = resp.get('error')
                if error:
                    print(f"  {provider}: ERROR - {error}")
                else:
                    response_text = resp.get('response', '')[:100]
                    print(f"  {provider}: SUCCESS - {response_text}...")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Compare endpoint error: {e}")

if __name__ == "__main__":
    test_api()
