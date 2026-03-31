import httpx
import os
from dotenv import load_dotenv

load_dotenv()

def list_google_models():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("No Google API key found")
        return
    
    try:
        with httpx.Client() as client:
            response = client.get(
                f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}",
                timeout=30.0
            )
            
            if response.status_code == 200:
                data = response.json()
                print("Available Google models:")
                for model in data.get('models', []):
                    name = model.get('name', 'Unknown')
                    display_name = model.get('displayName', 'No display name')
                    print(f"  {name} - {display_name}")
            else:
                print(f"Error listing models: {response.status_code}")
                print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_google_models()
