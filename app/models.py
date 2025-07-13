from pydantic import BaseModel
from typing import Dict, Any, Optional

class PromptRequest(BaseModel):
    """Request model for the generate endpoint."""
    prompt: str
    max_length: Optional[int] = None
    temperature: Optional[float] = None

class GenerateResponse(BaseModel):
    """Response model for the generate endpoint."""
    response: str

class ConfigRequest(BaseModel):
    """Request model for LLM configuration."""
    config: Dict[str, Any]