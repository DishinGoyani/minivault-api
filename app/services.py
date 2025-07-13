
import asyncio
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
from typing import Optional, Dict, Any
import logging

# Set up logging for the service module
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMService:
    """
    Service for handling local LLM (Large Language Model) operations.
    Loads and manages a HuggingFace transformer model for text generation.
    """

    def __init__(self, model_name: str = "Qwen/Qwen2-0.5B-Instruct"):
        """
        Initialize the LLMService instance and start loading the model asynchronously.

        Args:
            model_name (str): Name or path of the HuggingFace model to load.
        """
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.generator = None
        self.is_loaded = False
        self.config = {
            "max_length": 500,
            "temperature": 0.7,
            "do_sample": True,
            "pad_token_id": None
        }

        # Start loading model in background
        asyncio.create_task(self._load_model())

    async def _load_model(self):
        """
        Asynchronously load the tokenizer and model, and set up the text generation pipeline.
        Sets the pad token if not present and updates config accordingly.
        """
        try:
            logger.info(f"Loading model: {self.model_name}")

            # Load tokenizer and model from HuggingFace
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16,
                device_map="auto"
            )

            # Ensure pad_token is set
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token

            self.config["pad_token_id"] = self.tokenizer.pad_token_id

            # Create text generation pipeline
            self.generator = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                torch_dtype=torch.float32
            )

            self.is_loaded = True
            logger.info("Model loaded successfully!")

        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            self.is_loaded = False

    async def generate_response(self, prompt: str, **kwargs) -> str:
        """
        Generate a response using the loaded LLM model.

        Args:
            prompt (str): The input prompt for the model.
            **kwargs: Optional generation parameters to override defaults.

        Returns:
            str: The generated response text.
        """
        if not self.is_loaded:
            return "Model is still loading or failed to load. Please try again later."

        try:
            # Merge kwargs with default config
            generation_config = {**self.config, **kwargs}

            # Clean up the prompt
            prompt = prompt.strip()
            if not prompt:
                return "Please provide a valid prompt."

            # Format prompt for conversational context (system/user roles)
            messages = [
                {"role": "system", "content": "You are a helpful chat AI assistant."},
                {"role": "user", "content": prompt}
            ]
            # Convert messages to a single string for chat template
            formatted_prompt = "".join([
                f"<|system|>{m['content']}<|end|>" if m["role"] == "system" else f"<|user|>{m['content']}<|end|>" for m in messages
            ]) + "<|assistant|>"

            # Generate response using the pipeline in a thread executor
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: self.generator(
                    formatted_prompt,
                    max_length=generation_config["max_length"],
                    temperature=generation_config["temperature"],
                    do_sample=generation_config["do_sample"],
                    pad_token_id=generation_config["pad_token_id"],
                    num_return_sequences=1,
                    truncation=True
                )
            )

            # Extract the generated text
            generated_text = result[0]["generated_text"]

            # Remove the prompt from the response
            if generated_text.startswith(formatted_prompt):
                response = generated_text[len(formatted_prompt):].strip()
            else:
                response = generated_text.strip()

            # If response is empty or too short, provide a fallback
            if not response or len(response) < 5:
                response = "I understand your message. Could you please provide more context or ask a specific question?"

            return response

        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return f"Sorry, I encountered an error while generating a response: {str(e)}"

    def update_config(self, new_config: Dict[str, Any]):
        """
        Update the generation configuration for the LLMService.

        Args:
            new_config (Dict[str, Any]): Dictionary of config parameters to update.
        """
        self.config.update(new_config)
        logger.info(f"Configuration updated: {new_config}")

    def cleanup(self):
        """
        Clean up resources used by the LLMService, including model, tokenizer, and generator.
        Frees GPU memory if available.
        """
        if self.model:
            del self.model
        if self.tokenizer:
            del self.tokenizer
        if self.generator:
            del self.generator
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

def generate_stubbed_response(prompt: str) -> str:
    """
    Generate a stubbed response based on the input prompt.
    Used as a fallback when the LLM is not loaded.

    Args:
        prompt (str): The input prompt string.

    Returns:
        str: Simulated response text.
    """
    prompt_lower = prompt.lower()
    if "hello" in prompt_lower or "hi" in prompt_lower:
        return "Hello! I'm MiniVault, a simulated AI assistant. How can I help you today?"
    elif "weather" in prompt_lower:
        return "I'm a local API simulation, so I can't check real weather data. But I'd imagine it's a lovely day wherever you are!"
    elif "code" in prompt_lower or "programming" in prompt_lower:
        return "I'd love to help with coding! As a simulated response, I can suggest that breaking down problems into smaller steps is always a good approach."
    elif "explain" in prompt_lower:
        return f"You asked me to explain something about: '{prompt}'. In a real implementation, I would provide a detailed explanation based on my training data."
    elif len(prompt.strip()) == 0:
        return "It looks like you sent an empty prompt. Please provide some text for me to respond to!"
    else:
        return f"Thank you for your prompt: '{prompt[:50]}{'...' if len(prompt) > 50 else ''}'. This is a stubbed response from MiniVault API. In a real implementation, I would process your request using a language model."
