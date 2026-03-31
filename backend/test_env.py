import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("Testing environment variable loading:")
print(f"OPENAI_API_KEY exists: {bool(os.getenv('OPENAI_API_KEY'))}")
print(f"GOOGLE_API_KEY exists: {bool(os.getenv('GOOGLE_API_KEY'))}")
print(f"ANTHROPIC_API_KEY exists: {bool(os.getenv('ANTHROPIC_API_KEY'))}")
print(f"COHERE_API_KEY exists: {bool(os.getenv('COHERE_API_KEY'))}")

if os.getenv('OPENAI_API_KEY'):
    print(f"OpenAI key starts with: {os.getenv('OPENAI_API_KEY')[:10]}...")
if os.getenv('GOOGLE_API_KEY'):
    print(f"Google key starts with: {os.getenv('GOOGLE_API_KEY')[:10]}...")
