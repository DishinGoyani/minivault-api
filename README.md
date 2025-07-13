# MiniVault API

A lightweight local REST API that simulates ModelVault's core feature of receiving a prompt and returning a generated response. This implementation provides a stubbed (hardcoded) response system with comprehensive logging capabilities.

## Features

- **REST API Endpoint**: `POST /generate` for prompt processing
- **Automatic Logging**: All interactions logged to `logs/log.jsonl`
- **Health Monitoring**: Built-in health check endpoint
- **CORS Support**: Cross-origin requests enabled for frontend integration
- **Input Validation**: Pydantic models for request/response validation
- **Error Handling**: Comprehensive error handling with logging

## Project Structure

```
minivault-api/
├── logs/                  # Stores API interaction logs (JSONL format)
│   └── log.jsonl
├── app/                   # Core application code
│   ├── __init__.py
│   ├── main.py            # FastAPI app and endpoints
│   ├── models.py          # Pydantic models for requests/responses
│   ├── services.py        # Business logic (response generation)
│   ├── utils.py           # Utility functions (logging)
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
└── tests/                 # API test cases
   └── test_api.py
```

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project**:
   ```bash
   cd minivault-api
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the API

1. **Start the server**:
   ```bash
   python app.py
   ```
   
   Or alternatively:
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Verify the server is running**:
   - Open your browser and navigate to: `http://localhost:8000`
   - You should see a welcome message with API information

3. **Access the interactive API documentation**:
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## API Usage

### Endpoints

#### `GET /`
Returns basic API information and available endpoints.

**Response:**
```json
{
  "message": "Welcome to MiniVault API",
  "version": "1.0.0",
  "endpoints": {
    "generate": "POST /generate - Generate a response from a prompt"
  }
}
```

#### `GET /health`
Health check endpoint for monitoring API status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.000000"
}
```

#### `POST /generate`
Main endpoint for generating responses from prompts.

**Request:**
```json
{
  "prompt": "Hello, how are you?"
}
```

**Response:**
```json
{
  "response": "Hello! I'm MiniVault, a simulated AI assistant. How can I help you today?"
}
```

### Testing the API

#### Using curl

```bash
# Basic test
curl -X POST "http://localhost:8000/generate" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Hello, how are you?"}'

# Weather query
curl -X POST "http://localhost:8000/generate" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "What is the weather like today?"}'

# Programming question
curl -X POST "http://localhost:8000/generate" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Help me with Python code"}'
```

#### Using Python requests

```python
import requests

url = "http://localhost:8000/generate"
data = {"prompt": "Explain machine learning"}

response = requests.post(url, json=data)
print(response.json())
```

#### Using the Interactive Documentation

1. Navigate to `http://localhost:8000/docs`
2. Click on the `POST /generate` endpoint
3. Click "Try it out"
4. Enter your prompt in the request body
5. Click "Execute"

## Logging

All prompt-response interactions are automatically logged to `logs/log.jsonl`. Each log entry contains:

- **timestamp**: ISO format timestamp of the interaction
- **prompt**: The input prompt from the user
- **response**: The generated response

Example log entry:
```json
{"timestamp": "2024-01-15T10:30:00.000000", "prompt": "Hello", "response": "Hello! I'm MiniVault, a simulated AI assistant. How can I help you today?"}
```

## Implementation Notes

### Design Choices

1. **FastAPI Framework**: Chosen for its automatic API documentation, type validation, and modern async support.

2. **Stubbed Response Logic**: The current implementation uses simple keyword matching to provide contextually relevant stubbed responses:
   - Greetings ("hello", "hi") → Friendly welcome
   - Weather queries → Polite limitation acknowledgment
   - Code/programming → General coding advice
   - Explanation requests → Meta-explanation about the simulation
   - Default → Generic acknowledgment with prompt echo

3. **JSONL Logging**: Uses JSON Lines format for easy parsing and streaming log analysis.

4. **Error Handling**: Comprehensive error handling ensures all interactions (including errors) are logged.

### Tradeoffs

- **Simplicity vs. Sophistication**: Prioritized clear, maintainable code over complex response generation
- **Performance vs. Logging**: All requests are logged synchronously; for high-throughput scenarios, async logging would be beneficial
- **Memory vs. Disk**: Logs are written immediately to disk rather than buffered in memory

### Future Improvements

1. **Local LLM Integration**: Replace stubbed responses with actual language model inference using:
   - Hugging Face Transformers for lightweight models
   - Ollama for larger, more capable models
   - GGML/llama.cpp for efficient CPU inference

2. **Streaming Responses**: Implement Server-Sent Events (SSE) for token-by-token streaming

3. **Enhanced Logging**: Add structured logging with different log levels and rotation

4. **Configuration Management**: Environment-based configuration for different deployment scenarios

5. **Rate Limiting**: Implement request rate limiting for production use

6. **Authentication**: Add API key or token-based authentication

7. **Metrics and Monitoring**: Add Prometheus metrics for observability

## Development

### Code Structure

- **`app.py`**: Main application file containing all API logic
- **`PromptRequest`**: Pydantic model for input validation
- **`GenerateResponse`**: Pydantic model for response structure
- **`log_interaction()`**: Function handling all logging operations
- **`generate_stubbed_response()`**: Core logic for response generation

### Adding New Response Patterns

To add new stubbed response patterns, modify the `generate_stubbed_response()` function:

```python
def generate_stubbed_response(prompt: str) -> str:
    prompt_lower = prompt.lower()
    
    # Add your new pattern here
    if "your_keyword" in prompt_lower:
        return "Your custom response"
    
    # ... existing patterns
```

## License

This project is created as a take-home assignment for ModelVault and is intended for evaluation purposes.

