from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import httpx
import os
from dotenv import load_dotenv
import logging
from datetime import datetime
import urllib.parse

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {"message": "AnythingLibrary Backend is running", "status": "ok"}
            self.wfile.write(json.dumps(response).encode())
        elif self.path == '/test':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {"status": "working", "timestamp": datetime.now().isoformat()}
            self.wfile.write(json.dumps(response).encode())
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {"status": "healthy", "timestamp": datetime.now().isoformat()}
            self.wfile.write(json.dumps(response).encode())
        elif self.path == '/providers':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            providers = []
            if os.getenv("GOOGLE_API_KEY"):
                providers.append("google")
            if os.getenv("ANTHROPIC_API_KEY"):
                providers.append("anthropic")
            if os.getenv("GROQ_API_KEY"):
                providers.append("groq")
            if os.getenv("CEREBRAS_API_KEY"):
                providers.append("cerebras")
            # Temporarily disabled until correct models are identified
            # if os.getenv("COHERE_API_KEY"):
            #     providers.append("cohere")
            # if os.getenv("GROK_API_KEY"):
            #     providers.append("grok")
            
            logger.info(f"Available providers: {providers}")
            response = {"providers": providers}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {"detail": "Not Found"}
            self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        if self.path == '/login':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                username = data.get('username', '').strip()
                password = data.get('password', '').strip()
                
                if not username or not password:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    response = {"error": "Username and password are required"}
                    self.wfile.write(json.dumps(response).encode())
                    return
                
                # Simple authentication (you can modify this for real user management)
                # For demo purposes, accepting any non-empty username/password
                # In production, you'd verify against a database
                valid_credentials = (
                    len(username) >= 2 and 
                    len(password) >= 3 and
                    username.strip() and  # Just ensure it's not empty after stripping
                    password.strip() and   # Just ensure it's not empty after stripping
                    not username.isspace() and
                    not password.isspace()
                )
                
                if valid_credentials:
                    logger.info(f"User '{username}' logged in successfully")
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    response = {
                        "success": True,
                        "message": "Login successful",
                        "user": {
                            "username": username,
                            "login_time": datetime.now().isoformat()
                        }
                    }
                    self.wfile.write(json.dumps(response).encode())
                else:
                    logger.warning(f"Failed login attempt for username: '{username}'")
                    self.send_response(401)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    response = {"error": "Invalid username or password"}
                    self.wfile.write(json.dumps(response).encode())
                    
            except Exception as e:
                logger.error(f"Login error: {str(e)}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                response = {"error": "Login failed due to server error"}
                self.wfile.write(json.dumps(response).encode())
        elif self.path == '/compare':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                prompt = data.get('prompt', '')
                providers = data.get('providers', ['openai', 'google'])
                max_tokens = data.get('max_tokens', 500)
                temperature = data.get('temperature', 0.7)
                simplify = data.get('simplify', False)
                
                # If simplify is true, modify the prompt
                if simplify:
                    prompt = f"{prompt}\n\nPlease explain this like I'm 10 years old. Use simple words, short sentences, and examples that a child can understand. Avoid technical jargon and complex concepts."
                
                if not prompt.strip():
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    response = {"error": "Prompt cannot be empty"}
                    self.wfile.write(json.dumps(response).encode())
                    return
                
                logger.info(f"Received compare request: prompt='{prompt[:50]}...', providers={providers}")
                
                results = []
                
                if "google" in providers:
                    result = self.call_google(prompt, max_tokens, temperature)
                    results.append({
                        "provider": "google",
                        "response": result["response"],
                        "timestamp": datetime.now().isoformat(),
                        "tokens_used": result["tokens_used"],
                        "error": result["error"]
                    })
                
                if "groq" in providers:
                    result = self.call_groq(prompt, max_tokens, temperature)
                    results.append({
                        "provider": "groq",
                        "response": result["response"],
                        "timestamp": datetime.now().isoformat(),
                        "tokens_used": result["tokens_used"],
                        "error": result["error"]
                    })
                
                if "cerebras" in providers:
                    result = self.call_cerebras(prompt, max_tokens, temperature)
                    results.append({
                        "provider": "cerebras",
                        "response": result["response"],
                        "timestamp": datetime.now().isoformat(),
                        "tokens_used": result["tokens_used"],
                        "error": result["error"]
                    })
                
                if "cohere" in providers:
                    result = self.call_cohere(prompt, max_tokens, temperature)
                    results.append({
                        "provider": "cohere",
                        "response": result["response"],
                        "timestamp": datetime.now().isoformat(),
                        "tokens_used": result["tokens_used"],
                        "error": result["error"]
                    })
                
                if "grok" in providers:
                    result = self.call_grok(prompt, max_tokens, temperature)
                    results.append({
                        "provider": "grok",
                        "response": result["response"],
                        "timestamp": datetime.now().isoformat(),
                        "tokens_used": result["tokens_used"],
                        "error": result["error"]
                    })
                
                logger.info(f"Returning {len(results)} responses")
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                response = {
                    "prompt": prompt,
                    "responses": results,
                    "timestamp": datetime.now().isoformat()
                }
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                logger.error(f"Error in compare endpoint: {str(e)}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                response = {"error": str(e)}
                self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {"detail": "Not Found"}
            self.wfile.write(json.dumps(response).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def call_google(self, prompt: str, max_tokens: int = 1500, temperature: float = 0.7):
        try:
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                return {"response": "", "tokens_used": None, "error": "Google API key not configured"}
            
            with httpx.Client() as client:
                response = client.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}",
                    headers={"Content-Type": "application/json"},
                    json={
                        "contents": [{"parts": [{"text": f"{prompt}\n\nIMPORTANT: Please provide a complete, detailed response. Do not stop mid-sentence. Include multiple paragraphs with examples and explanations. Write at least 3-5 paragraphs covering the topic thoroughly."}]}],
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
                    logger.info(f"Google response length: {len(google_response)} characters")
                    logger.info(f"Google response preview: {google_response[:200]}...")
                    return {
                        "response": google_response,
                        "tokens_used": None,
                        "error": None
                    }
                else:
                    return {
                        "response": "",
                        "tokens_used": None,
                        "error": f"Google API error: {response.status_code} - {response.text}"
                    }
        except Exception as e:
            return {
                "response": "",
                "tokens_used": None,
                "error": f"Google connection error: {str(e)}"
            }
    
    def call_groq(self, prompt: str, max_tokens: int = 300, temperature: float = 0.7):
        try:
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                return {"response": "", "tokens_used": None, "error": "GROQ API key not configured"}
            
            with httpx.Client() as client:
                response = client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
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
                    return {
                        "response": data["choices"][0]["message"]["content"],
                        "tokens_used": data.get("usage", {}).get("total_tokens"),
                        "error": None
                    }
                else:
                    return {
                        "response": "",
                        "tokens_used": None,
                        "error": f"GROQ API error: {response.status_code} - {response.text}"
                    }
        except Exception as e:
            return {
                "response": "",
                "tokens_used": None,
                "error": f"GROQ connection error: {str(e)}"
            }
    
    def call_cerebras(self, prompt: str, max_tokens: int = 300, temperature: float = 0.7):
        try:
            api_key = os.getenv("CEREBRAS_API_KEY")
            if not api_key:
                return {"response": "", "tokens_used": None, "error": "Cerebras API key not configured"}
            
            with httpx.Client() as client:
                response = client.post(
                    "https://api.cerebras.ai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
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
                    return {
                        "response": data["choices"][0]["message"]["content"],
                        "tokens_used": data.get("usage", {}).get("total_tokens"),
                        "error": None
                    }
                else:
                    return {
                        "response": "",
                        "tokens_used": None,
                        "error": f"Cerebras API error: {response.status_code} - {response.text}"
                    }
        except Exception as e:
            return {
                "response": "",
                "tokens_used": None,
                "error": f"Cerebras connection error: {str(e)}"
            }
    
    def call_cohere(self, prompt: str, max_tokens: int = 500, temperature: float = 0.7):
        try:
            api_key = os.getenv("COHERE_API_KEY")
            if not api_key:
                return {"response": "", "tokens_used": None, "error": "Cohere API key not configured"}
            
            with httpx.Client() as client:
                response = client.post(
                    "https://api.cohere.ai/v1/chat",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                        "Accept": "application/json"
                    },
                    json={
                        "model": "c4ai-command-r-plus-08-2024",
                        "message": prompt,
                        "max_tokens": max_tokens,
                        "temperature": temperature,
                        "k": 0,
                        "stop_sequences": [],
                        "return_likelihoods": "NONE"
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "response": data["text"],
                        "tokens_used": data.get("token_count", {}).get("input_tokens") + data.get("token_count", {}).get("output_tokens"),
                        "error": None
                    }
                else:
                    return {
                        "response": "",
                        "tokens_used": None,
                        "error": f"Cohere API error: {response.status_code} - {response.text}"
                    }
        except Exception as e:
            return {
                "response": "",
                "tokens_used": None,
                "error": f"Cohere connection error: {str(e)}"
            }
    
    def call_grok(self, prompt: str, max_tokens: int = 500, temperature: float = 0.7):
        try:
            api_key = os.getenv("GROK_API_KEY")
            if not api_key:
                return {"response": "", "tokens_used": None, "error": "Grok API key not configured"}
            
            with httpx.Client() as client:
                response = client.post(
                    "https://api.x.ai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "grok-2-public",
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
                        "tokens_used": data.get("usage", {}).get("total_tokens"),
                        "error": None
                    }
                else:
                    return {
                        "response": "",
                        "tokens_used": None,
                        "error": f"Grok API error: {response.status_code} - {response.text}"
                    }
        except Exception as e:
            return {
                "response": "",
                "tokens_used": None,
                "error": f"Grok connection error: {str(e)}"
            }
    
    def log_message(self, format, *args):
        logger.info(f"{self.address_string()} - {format % args}")

if __name__ == "__main__":
    server_address = ('', 8001)
    httpd = HTTPServer(server_address, APIHandler)
    logger.info("Starting AnythingLibrary Simple HTTP Server on port 8001...")
    httpd.serve_forever()
