from pydantic import BaseModel

class PromptRequest(BaseModel):
    """Request model for the generate endpoint."""
    prompt: str

class GenerateResponse(BaseModel):
    """Response model for the generate endpoint."""
    response: str
