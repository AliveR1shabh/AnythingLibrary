from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import asyncio
import httpx
import os
from dotenv import load_dotenv
import logging
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AnythingLibrary API",
    description="Multi-AI comparison API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class AIRequest(BaseModel):
    prompt: str
    providers: List[str] = ["google", "groq", "cerebras"]
    max_tokens: Optional[int] = 1500
    temperature: Optional[float] = 0.7
    simplify: Optional[bool] = False

class AIResponse(BaseModel):
    provider: str
    response: str
    timestamp: datetime
    tokens_used: Optional[int] = None
    error: Optional[str] = None

class ComparisonResult(BaseModel):
    prompt: str
    responses: List[AIResponse]
    timestamp: datetime

# AI Providers
class AIProvider:
    def __init__(self, name: str, api_key: str):
        self.name = name
        self.api_key = api_key
    
    async def generate_response(self, prompt: str, max_tokens: int = 500, temperature: float = 0.7) -> Dict[str, Any]:
        raise NotImplementedError

class OpenAIProvider(AIProvider):
    async def generate_response(self, prompt: str, max_tokens: int = 500, temperature: float = 0.7) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
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

class AnthropicProvider(AIProvider):
    async def generate_response(self, prompt: str, max_tokens: int = 500, temperature: float = 0.7) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": self.api_key,
                        "Content-Type": "application/json",
                        "anthropic-version": "2023-06-01"
                    },
                    json={
                        "model": "claude-3-haiku-20240307",
                        "max_tokens": max_tokens,
                        "temperature": temperature,
                        "messages": [{"role": "user", "content": prompt}]
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "response": data["content"][0]["text"],
                        "tokens_used": data["usage"]["input_tokens"] + data["usage"]["output_tokens"],
                        "error": None
                    }
                else:
                    return {
                        "response": "",
                        "tokens_used": None,
                        "error": f"Anthropic API error: {response.status_code}"
                    }
        except Exception as e:
            return {
                "response": "",
                "tokens_used": None,
                "error": f"Anthropic connection error: {str(e)}"
            }

class GoogleProvider(AIProvider):
    async def generate_response(self, prompt: str, max_tokens: int = 1500, temperature: float = 0.7) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={self.api_key}",
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
                    return {
                        "response": google_response,
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

class GroqProvider(AIProvider):
    async def generate_response(self, prompt: str, max_tokens: int = 300, temperature: float = 0.7) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
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
                        "error": f"GROQ API error: {response.status_code}"
                    }
        except Exception as e:
            return {
                "response": "",
                "tokens_used": None,
                "error": f"GROQ connection error: {str(e)}"
            }

class CerebrasProvider(AIProvider):
    async def generate_response(self, prompt: str, max_tokens: int = 300, temperature: float = 0.7) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.cerebras.ai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
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
                        "error": f"Cerebras API error: {response.status_code}"
                    }
        except Exception as e:
            return {
                "response": "",
                "tokens_used": None,
                "error": f"Cerebras connection error: {str(e)}"
            }

class CohereProvider(AIProvider):
    async def generate_response(self, prompt: str, max_tokens: int = 500, temperature: float = 0.7) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.cohere.ai/v1/generate",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "command",
                        "prompt": prompt,
                        "max_tokens": max_tokens,
                        "temperature": temperature
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "response": data["generations"][0]["text"],
                        "tokens_used": data["meta"]["billed_units"]["output_tokens"] + data["meta"]["billed_units"]["input_tokens"],
                        "error": None
                    }
                else:
                    return {
                        "response": "",
                        "tokens_used": None,
                        "error": f"Cohere API error: {response.status_code}"
                    }
        except Exception as e:
            return {
                "response": "",
                "tokens_used": None,
                "error": f"Cohere connection error: {str(e)}"
            }

# Initialize providers
def get_providers() -> Dict[str, AIProvider]:
    providers = {}
    
    logger.info("Checking for API keys...")
    
    if os.getenv("GOOGLE_API_KEY"):
        providers["google"] = GoogleProvider("Google", os.getenv("GOOGLE_API_KEY"))
        logger.info("Google provider initialized")
    else:
        logger.warning("Google API key not found")
    
    if os.getenv("GROQ_API_KEY"):
        providers["groq"] = GroqProvider("GROQ", os.getenv("GROQ_API_KEY"))
        logger.info("GROQ provider initialized")
    else:
        logger.warning("GROQ API key not found")
    
    if os.getenv("CEREBRAS_API_KEY"):
        providers["cerebras"] = CerebrasProvider("Cerebras", os.getenv("CEREBRAS_API_KEY"))
        logger.info("Cerebras provider initialized")
    else:
        logger.warning("Cerebras API key not found")
    
    logger.info(f"Total providers available: {list(providers.keys())}")
    return providers

# Routes
@app.get("/")
async def root():
    return {"message": "AnythingLibrary API is running"}

@app.get("/test")
async def test():
    return {"status": "working", "env_loaded": bool(os.getenv("OPENAI_API_KEY"))}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

@app.get("/providers")
async def get_available_providers():
    providers = get_providers()
    return {"providers": list(providers.keys())}

@app.post("/compare", response_model=ComparisonResult)
async def compare_ai_responses(request: AIRequest):
    prompt = request.prompt
    providers = request.providers
    max_tokens = request.max_tokens
    temperature = request.temperature
    simplify = request.simplify
    
    if not prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    
    # If simplify is true, modify the prompt
    if simplify:
        prompt = f"{prompt}\n\nPlease explain this like I'm 10 years old. Use simple words, short sentences, and examples that a child can understand. Avoid technical jargon and complex concepts."
    
    logger.info(f"Received compare request: prompt='{prompt[:50]}...', providers={providers}")
    
    providers_dict = get_providers()
    logger.info(f"Available providers: {list(providers_dict.keys())}")
    
    # Filter providers based on request and availability
    available_providers = {}
    for provider_name in providers:
        if provider_name in providers_dict:
            available_providers[provider_name] = providers_dict[provider_name]
            logger.info(f"Provider {provider_name} is available")
        else:
            logger.warning(f"Provider {provider_name} requested but not available")
    
    if not available_providers:
        logger.error("No AI providers available for this request")
        raise HTTPException(status_code=400, detail="No AI providers available")
    
    logger.info(f"Making parallel API calls to {list(available_providers.keys())}")
    
    # Make parallel API calls
    tasks = []
    for provider_name, provider in available_providers.items():
        task = provider.generate_response(
            prompt, 
            max_tokens, 
            temperature
        )
        tasks.append((provider_name, task))
    
    # Wait for all responses
    results = []
    responses = await asyncio.gather(*[task for _, task in tasks])
    
    for (provider_name, _), response_data in zip(tasks, responses):
        logger.info(f"Response from {provider_name}: {response_data['error'] or 'Success'}")
        ai_response = AIResponse(
            provider=provider_name,
            response=response_data["response"],
            timestamp=datetime.now(),
            tokens_used=response_data["tokens_used"],
            error=response_data["error"]
        )
        results.append(ai_response)
    
    logger.info(f"Returning {len(results)} responses")
    return ComparisonResult(
        prompt=request.prompt,  # Use original prompt, not modified one
        responses=results,
        timestamp=datetime.now()
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
