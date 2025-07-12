from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import PromptRequest, GenerateResponse
from .services import generate_stubbed_response
from .utils import log_interaction
from datetime import datetime

app = FastAPI(
    title="MiniVault API",
    description="A lightweight local REST API that simulates ModelVault's core feature",
    version="1.0.0"
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
        "version": "1.0.0",
        "endpoints": {
            "generate": "POST /generate - Generate a response from a prompt"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.post("/generate", response_model=GenerateResponse)
async def generate(request: PromptRequest) -> GenerateResponse:
    try:
        response_text = generate_stubbed_response(request.prompt)
        log_interaction(request.prompt, response_text)
        return GenerateResponse(response=response_text)
    except Exception as e:
        error_response = f"Error processing request: {str(e)}"
        log_interaction(request.prompt, error_response)
        raise HTTPException(status_code=500, detail=error_response)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
