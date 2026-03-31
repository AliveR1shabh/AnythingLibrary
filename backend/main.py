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
    providers: List[str] = ["openai", "anthropic", "google", "cohere"]
    max_tokens: Optional[int] = 500
    temperature: Optional[float] = 0.7

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
    async def generate_response(self, prompt: str, max_tokens: int = 500, temperature: float = 0.7) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={self.api_key}",
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
                        "tokens_used": None,  # Google doesn't provide token count in the same way
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
    
    if os.getenv("OPENAI_API_KEY"):
        providers["openai"] = OpenAIProvider("OpenAI", os.getenv("OPENAI_API_KEY"))
        logger.info("OpenAI provider initialized")
    else:
        logger.warning("OpenAI API key not found")
    
    if os.getenv("ANTHROPIC_API_KEY"):
        providers["anthropic"] = AnthropicProvider("Anthropic", os.getenv("ANTHROPIC_API_KEY"))
        logger.info("Anthropic provider initialized")
    else:
        logger.warning("Anthropic API key not found")
    
    if os.getenv("GOOGLE_API_KEY"):
        providers["google"] = GoogleProvider("Google", os.getenv("GOOGLE_API_KEY"))
        logger.info("Google provider initialized")
    else:
        logger.warning("Google API key not found")
    
    if os.getenv("COHERE_API_KEY"):
        providers["cohere"] = CohereProvider("Cohere", os.getenv("COHERE_API_KEY"))
        logger.info("Cohere provider initialized")
    else:
        logger.warning("Cohere API key not found")
    
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
    logger.info(f"Received compare request: prompt='{request.prompt[:50]}...', providers={request.providers}")
    
    providers = get_providers()
    logger.info(f"Available providers: {list(providers.keys())}")
    
    # Filter providers based on request and availability
    available_providers = {}
    for provider_name in request.providers:
        if provider_name in providers:
            available_providers[provider_name] = providers[provider_name]
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
            request.prompt, 
            request.max_tokens, 
            request.temperature
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
        prompt=request.prompt,
        responses=results,
        timestamp=datetime.now()
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
