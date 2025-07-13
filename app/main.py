"""
main.py
--------
Entry point for the MiniVault API using FastAPI.
Defines endpoints for LLM interaction, configuration, and health checks.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import PromptRequest, GenerateResponse, ConfigRequest
from app.services import LLMService, generate_stubbed_response
from app.utils import log_interaction
from datetime import datetime, timezone
from contextlib import asynccontextmanager

# Global LLM service instance
llm_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan context manager for startup and shutdown events.
    Initializes and cleans up the global LLM service instance.
    """
    global llm_service
    llm_service = LLMService()
    yield
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
    """
    Root endpoint providing API info and available features.
    """
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
    """
    Health check endpoint.
    Returns API status and LLM loaded state.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "llm_loaded": llm_service.is_loaded if llm_service else False
    }

@app.post("/generate", response_model=GenerateResponse)
async def generate(request: PromptRequest) -> GenerateResponse:
    """
    Generate a response from the LLM based on the provided prompt.
    Falls back to a stubbed response if LLM is not loaded.
    Args:
        request (PromptRequest): The prompt request payload.
    Returns:
        GenerateResponse: The generated response object.
    """
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
    """
    Configure LLM settings such as temperature, max_length, etc.
    Args:
        request (ConfigRequest): Configuration parameters for the LLM.
    Returns:
        dict: Status and message about configuration update.
    """
    try:
        if llm_service:
            llm_service.update_config(request.config)
            return {
                "status": "success",
                "message": "Configuration updated",
                "example": {
                    "config": {
                        "temperature": "float (e.g. 0.7)",
                        "max_length": "int (e.g. 256)",
                    }
                }
            }
        else:
            return {
                "status": "error",
                "message": "LLM service not available"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Configuration error: {str(e)}")

if __name__ == "__main__":
    # Run the FastAPI app using Uvicorn for local development
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
