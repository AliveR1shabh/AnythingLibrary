import requests
import json

def test_google_only():
    base_url = "http://localhost:8001"
    
    print("Testing Google API only...")
    
    try:
        test_data = {
            "prompt": "What is 2+2? Give a short answer.",
            "providers": ["google"],  # Only test Google
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
                    response_text = resp.get('response', '')[:200]
                    print(f"  {provider}: SUCCESS - {response_text}...")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Compare endpoint error: {e}")

if __name__ == "__main__":
    test_google_only()
