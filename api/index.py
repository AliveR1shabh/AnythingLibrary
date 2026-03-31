import json
import httpx
import os
from datetime import datetime

# Load environment variables (Vercel handles this automatically)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY")

def handler(request):
    try:
        # Parse request body
        if request.method == "OPTIONS":
            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type",
                },
                "body": ""
            }
        
        if request.method != "POST":
            return {
                "statusCode": 405,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Method not allowed"})
            }
        
        body = json.loads(request.body)
        prompt = body.get("prompt", "")
        providers = body.get("providers", ["google", "groq", "cerebras"])
        max_tokens = body.get("max_tokens", 1500)
        temperature = body.get("temperature", 0.7)
        simplify = body.get("simplify", False)
        
        if not prompt.strip():
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Prompt cannot be empty"})
            }
        
        # If simplify is true, modify the prompt
        if simplify:
            prompt = f"{prompt}\n\nPlease explain this like I'm 10 years old. Use simple words, short sentences, and examples that a child can understand. Avoid technical jargon and complex concepts."
        
        # Process responses synchronously for Vercel
        results = []
        
        # Google API call
        if "google" in providers and GOOGLE_API_KEY:
            try:
                response = httpx.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GOOGLE_API_KEY}",
                    headers={"Content-Type": "application/json"},
                    json={
                        "contents": [{"parts": [{"text": prompt}]}],
                        "generationConfig": {
                            "maxOutputTokens": max_tokens,
                            "temperature": temperature,
                            "topP": 0.9,
                            "topK": 40,
                            "candidateCount": 1,
                            "stopSequences": []
                        }
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    google_response = data["candidates"][0]["content"]["parts"][0]["text"]
                    results.append({
                        "provider": "google",
                        "response": google_response,
                        "timestamp": datetime.now().isoformat(),
                        "tokens_used": None,
                        "error": None
                    })
                else:
                    results.append({
                        "provider": "google",
                        "response": "",
                        "timestamp": datetime.now().isoformat(),
                        "tokens_used": None,
                        "error": f"Google API error: {response.status_code}"
                    })
            except Exception as e:
                results.append({
                    "provider": "google",
                    "response": "",
                    "timestamp": datetime.now().isoformat(),
                    "tokens_used": None,
                    "error": f"Google connection error: {str(e)}"
                })
        
        # GROQ API call
        if "groq" in providers and GROQ_API_KEY:
            try:
                response = httpx.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {GROQ_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "llama-3.3-70b-versatile",
                        "messages": [{"role": "user", "content": prompt}],
                        "max_tokens": max_tokens,
                        "temperature": temperature
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    results.append({
                        "provider": "groq",
                        "response": data["choices"][0]["message"]["content"],
                        "timestamp": datetime.now().isoformat(),
                        "tokens_used": data.get("usage", {}).get("total_tokens"),
                        "error": None
                    })
                else:
                    results.append({
                        "provider": "groq",
                        "response": "",
                        "timestamp": datetime.now().isoformat(),
                        "tokens_used": None,
                        "error": f"GROQ API error: {response.status_code}"
                    })
            except Exception as e:
                results.append({
                    "provider": "groq",
                    "response": "",
                    "timestamp": datetime.now().isoformat(),
                    "tokens_used": None,
                    "error": f"GROQ connection error: {str(e)}"
                })
        
        # Cerebras API call
        if "cerebras" in providers and CEREBRAS_API_KEY:
            try:
                response = httpx.post(
                    "https://api.cerebras.ai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {CEREBRAS_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "llama3.1-8b",
                        "messages": [{"role": "user", "content": prompt}],
                        "max_tokens": max_tokens,
                        "temperature": temperature
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    results.append({
                        "provider": "cerebras",
                        "response": data["choices"][0]["message"]["content"],
                        "timestamp": datetime.now().isoformat(),
                        "tokens_used": data.get("usage", {}).get("total_tokens"),
                        "error": None
                    })
                else:
                    results.append({
                        "provider": "cerebras",
                        "response": "",
                        "timestamp": datetime.now().isoformat(),
                        "tokens_used": None,
                        "error": f"Cerebras API error: {response.status_code}"
                    })
            except Exception as e:
                results.append({
                    "provider": "cerebras",
                    "response": "",
                    "timestamp": datetime.now().isoformat(),
                    "tokens_used": None,
                    "error": f"Cerebras connection error: {str(e)}"
                })
        
        response_data = {
            "prompt": body.get("prompt", ""),
            "responses": results,
            "timestamp": datetime.now().isoformat()
        }
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
            },
            "body": json.dumps(response_data)
        }
        
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": f"Internal server error: {str(e)}"})
        }
