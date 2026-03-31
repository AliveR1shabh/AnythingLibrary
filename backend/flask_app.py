from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
import httpx
import os
from dotenv import load_dotenv
import logging
from datetime import datetime
import nest_asyncio

# Apply nest_asyncio to allow asyncio in Flask
nest_asyncio.apply()

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])

# Simple AI API functions
async def call_openai(prompt: str, max_tokens: int = 500, temperature: float = 0.7):
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return {"response": "", "tokens_used": None, "error": "OpenAI API key not configured"}
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": max_tokens,
                    "temperature": temperature
                },
                timeout=30.0
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "response": data["choices"][0]["message"]["content"],
                    "tokens_used": data["usage"]["total_tokens"],
                    "error": None
                }
            else:
                return {
                    "response": "",
                    "tokens_used": None,
                    "error": f"OpenAI API error: {response.status_code}"
                }
    except Exception as e:
        return {
            "response": "",
            "tokens_used": None,
            "error": f"OpenAI connection error: {str(e)}"
        }

async def call_google(prompt: str, max_tokens: int = 500, temperature: float = 0.7):
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return {"response": "", "tokens_used": None, "error": "Google API key not configured"}
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}",
                headers={"Content-Type": "application/json"},
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {
                        "maxOutputTokens": max_tokens,
                        "temperature": temperature
                    }
                },
                timeout=30.0
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "response": data["candidates"][0]["content"]["parts"][0]["text"],
                    "tokens_used": None,
                    "error": None
                }
            else:
                return {
                    "response": "",
                    "tokens_used": None,
                    "error": f"Google API error: {response.status_code}"
                }
    except Exception as e:
        return {
            "response": "",
            "tokens_used": None,
            "error": f"Google connection error: {str(e)}"
        }

# Routes
@app.route('/')
def root():
    return jsonify({"message": "AnythingLibrary Backend is running", "status": "ok"})

@app.route('/test')
def test():
    return jsonify({"status": "working", "timestamp": datetime.now().isoformat()})

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/providers')
def get_available_providers():
    providers = []
    if os.getenv("OPENAI_API_KEY"):
        providers.append("openai")
    if os.getenv("GOOGLE_API_KEY"):
        providers.append("google")
    if os.getenv("ANTHROPIC_API_KEY"):
        providers.append("anthropic")
    if os.getenv("COHERE_API_KEY"):
        providers.append("cohere")
    
    logger.info(f"Available providers: {providers}")
    return jsonify({"providers": providers})

@app.route('/compare', methods=['POST'])
def compare_ai_responses():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        providers = data.get('providers', ['openai', 'google'])
        max_tokens = data.get('max_tokens', 500)
        temperature = data.get('temperature', 0.7)
        
        logger.info(f"Received compare request: prompt='{prompt[:50]}...', providers={providers}")
        
        # Run async functions
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        results = []
        
        if "openai" in providers:
            result = loop.run_until_complete(call_openai(prompt, max_tokens, temperature))
            results.append({
                "provider": "openai",
                "response": result["response"],
                "timestamp": datetime.now().isoformat(),
                "tokens_used": result["tokens_used"],
                "error": result["error"]
            })
        
        if "google" in providers:
            result = loop.run_until_complete(call_google(prompt, max_tokens, temperature))
            results.append({
                "provider": "google",
                "response": result["response"],
                "timestamp": datetime.now().isoformat(),
                "tokens_used": result["tokens_used"],
                "error": result["error"]
            })
        
        loop.close()
        
        logger.info(f"Returning {len(results)} responses")
        
        return jsonify({
            "prompt": prompt,
            "responses": results,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in compare endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    logger.info("Starting AnythingLibrary Flask API...")
    app.run(host="0.0.0.0", port=8000, debug=True)
