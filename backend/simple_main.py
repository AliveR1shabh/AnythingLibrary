from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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
    providers: List[str] = ["openai", "google"]
    max_tokens: Optional[int] = 500
    temperature: Optional[float] = 0.7

class AIResponse(BaseModel):
    provider: str
    response: str
    timestamp: str
    tokens_used: Optional[int] = None
    error: Optional[str] = None

class ComparisonResult(BaseModel):
    prompt: str
    responses: List[AIResponse]
    timestamp: str

# Simple AI API functions
async def call_openai(prompt: str, max_tokens: int = 500, temperature: float = 0.7) -> Dict[str, Any]:
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
                    "error": f"OpenAI API error: {response.status_code} - {response.text}"
                }
    except Exception as e:
        return {
            "response": "",
            "tokens_used": None,
            "error": f"OpenAI connection error: {str(e)}"
        }

async def call_google(prompt: str, max_tokens: int = 500, temperature: float = 0.7) -> Dict[str, Any]:
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
                    "error": f"Google API error: {response.status_code} - {response.text}"
                }
    except Exception as e:
        return {
            "response": "",
            "tokens_used": None,
            "error": f"Google connection error: {str(e)}"
        }

# Routes
@app.get("/")
async def root():
    return {"message": "AnythingLibrary API is running", "status": "ok"}

@app.get("/test")
async def test():
    return {"status": "working", "timestamp": datetime.now().isoformat()}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/providers")
async def get_available_providers():
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
    return {"providers": providers}

@app.post("/compare", response_model=ComparisonResult)
async def compare_ai_responses(request: AIRequest):
    logger.info(f"Received compare request: prompt='{request.prompt[:50]}...', providers={request.providers}")
    
    results = []
    
    # Make API calls based on requested providers
    tasks = []
    
    if "openai" in request.providers:
        tasks.append(("openai", call_openai(request.prompt, request.max_tokens, request.temperature)))
    
    if "google" in request.providers:
        tasks.append(("google", call_google(request.prompt, request.max_tokens, request.temperature)))
    
    if not tasks:
        raise HTTPException(status_code=400, detail="No valid providers specified")
    
    # Execute all API calls
    responses = await asyncio.gather(*[task for _, task in tasks], return_exceptions=True)
    
    for (provider_name, _), response in zip(tasks, responses):
        if isinstance(response, Exception):
            logger.error(f"Exception from {provider_name}: {str(response)}")
            ai_response = AIResponse(
                provider=provider_name,
                response="",
                timestamp=datetime.now().isoformat(),
                tokens_used=None,
                error=f"Exception: {str(response)}"
            )
        else:
            logger.info(f"Response from {provider_name}: {response.get('error') or 'Success'}")
            ai_response = AIResponse(
                provider=provider_name,
                response=response["response"],
                timestamp=datetime.now().isoformat(),
                tokens_used=response["tokens_used"],
                error=response["error"]
            )
        results.append(ai_response)
    
    logger.info(f"Returning {len(results)} responses")
    
    return ComparisonResult(
        prompt=request.prompt,
        responses=results,
        timestamp=datetime.now().isoformat()
    )

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting AnythingLibrary API...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
