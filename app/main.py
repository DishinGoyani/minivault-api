from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import PromptRequest, GenerateResponse, ConfigRequest
from services import LLMService, generate_stubbed_response
from utils import log_interaction
from datetime import datetime
from contextlib import asynccontextmanager

# Global LLM service instance
llm_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global llm_service
    llm_service = LLMService()
    yield
    # Shutdown
    if llm_service:
        llm_service.cleanup()

app = FastAPI(
    title="MiniVault API",
    description="A lightweight local REST API with real LLM capabilities",
    version="2.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Welcome to MiniVault API",
        "version": "2.0.0",
        "features": {
            "local_llm": llm_service.is_loaded if llm_service else False,
            "model": llm_service.model_name if llm_service and llm_service.is_loaded else "None"
        },
        "endpoints": {
            "generate": "POST /generate - Generate a response from a prompt",
            "config": "POST /config - Configure LLM settings",
            "health": "GET /health - Health check"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "llm_loaded": llm_service.is_loaded if llm_service else False
    }

@app.post("/generate", response_model=GenerateResponse)
async def generate(request: PromptRequest) -> GenerateResponse:
    try:
        # Try to use local LLM first, fallback to stubbed response
        if llm_service and llm_service.is_loaded:
            response_text = await llm_service.generate_response(request.prompt)
        else:
            response_text = generate_stubbed_response(request.prompt)
            response_text += " (Note: Using stubbed response - LLM not loaded)"
        
        log_interaction(request.prompt, response_text)
        return GenerateResponse(response=response_text)
    except Exception as e:
        error_response = f"Error processing request: {str(e)}"
        log_interaction(request.prompt, error_response)
        raise HTTPException(status_code=500, detail=error_response)

@app.post("/config")
async def configure_llm(request: ConfigRequest):
    """Configure LLM settings like temperature, max_length, etc."""
    try:
        if llm_service:
            llm_service.update_config(request.config)
            return {"status": "success", "message": "Configuration updated"}
        else:
            return {"status": "error", "message": "LLM service not available"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Configuration error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
