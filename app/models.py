
# models.py
# ---------
# Defines Pydantic models for request and response payloads used in the MiniVault API.

from pydantic import BaseModel
from typing import Dict, Any, Optional


class PromptRequest(BaseModel):
    """
    Request model for the /generate endpoint.
    Attributes:
        prompt (str): The input prompt for the LLM.
        max_length (Optional[int]): Maximum length of the generated response.
        temperature (Optional[float]): Sampling temperature for response generation.
    """
    prompt: str
    max_length: Optional[int] = None
    temperature: Optional[float] = None


class GenerateResponse(BaseModel):
    """
    Response model for the /generate endpoint.
    Attributes:
        response (str): The generated text from the LLM.
    """
    response: str


class ConfigRequest(BaseModel):
    """
    Request model for LLM configuration via /config endpoint.
    Attributes:
        config (Dict[str, Any]): Dictionary of configuration parameters for the LLM.
    """
    config: Dict[str, Any]