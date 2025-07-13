
#!/usr/bin/env python3
"""
Enhanced test script for MiniVault API with LLM capabilities.
This script performs integration tests on the API endpoints, including health, configuration,
and LLM-based text generation. Results are printed to the console for manual inspection.
"""

import requests
import json
import time

API_BASE_URL = "http://localhost:8000"  # Base URL for the MiniVault API

def test_api():
    """
    Run integration tests for the MiniVault API endpoints.

    This function tests:
        1. Root endpoint
        2. Health endpoint
        3. Configuration endpoint
        4. Generate endpoint with various prompts
        5. Generate endpoint with custom parameters
    Prints results to the console for each test.
    """
    print("🧪 Testing Enhanced MiniVault API with LLM")
    print("=" * 60)

    # 1. Test root endpoint
    print("\n1. Testing root endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except requests.exceptions.ConnectionError:
        print("❌ Server not running. Please start the server first with: python main.py")
        return

    # 2. Test health endpoint
    print("\n2. Testing health endpoint...")
    response = requests.get(f"{API_BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    # 3. Test configuration endpoint
    print("\n3. Testing configuration endpoint...")
    config_data = {
        "config": {
            "temperature": 0.8,
            "max_length": 150
        }
    }
    response = requests.post(f"{API_BASE_URL}/config", json=config_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    # 4. Test generate endpoint with various prompts
    test_prompts = [
        "Hello, how are you?",
        "Tell me a short joke",
        "What is artificial intelligence?",
        "Help me understand machine learning",
        "Write a haiku about programming",
        "Explain quantum computing in simple terms",
        ""  # Empty prompt test
    ]

    print("\n4. Testing generate endpoint with various prompts...")
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n4.{i} Testing prompt: '{prompt}'")

        data = {"prompt": prompt}
        response = requests.post(f"{API_BASE_URL}/generate", json=data)

        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            # Print only the generated response for clarity
            print(f"Response: {result.get('response', '')}")
        else:
            print(f"Error: {response.text}")

        time.sleep(1)  # Delay to avoid overwhelming the API/model

    # 5. Test generate endpoint with custom parameters
    print("\n5. Testing with custom parameters...")
    custom_data = {
        "prompt": "Write a creative story about a robot",
        "max_length": 200,
        "temperature": 0.9
    }
    response = requests.post(f"{API_BASE_URL}/generate", json=custom_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Creative Response: {result.get('response', '')}")
    else:
        print(f"Error: {response.text}")

    print("\n✅ Enhanced API testing completed!")
    print("\n📝 Check logs/log.jsonl for logged interactions")
    print("💡 Note: First few requests might be slower while the model loads")


if __name__ == "__main__":
    test_api()