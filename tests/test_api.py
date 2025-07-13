#!/usr/bin/env python3
"""
Enhanced test script for MiniVault API with LLM capabilities
"""
import requests
import json
import time

API_BASE_URL = "http://localhost:8000"

def test_api():
    """Test the enhanced MiniVault API endpoints"""
    
    print("🧪 Testing Enhanced MiniVault API with LLM")
    print("=" * 60)
    
    # Test root endpoint
    print("\n1. Testing root endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except requests.exceptions.ConnectionError:
        print("❌ Server not running. Please start the server first with: python main.py")
        return
    
    # Test health endpoint
    print("\n2. Testing health endpoint...")
    response = requests.get(f"{API_BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test configuration endpoint
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
    
    # Test generate endpoint with various prompts
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
            print(f"Response: {result['response']}")
        else:
            print(f"Error: {response.text}")
        
        time.sleep(1)  # Slightly longer delay for LLM processing
    
    # Test with custom parameters
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
        print(f"Creative Response: {result['response']}")
    
    print("\n✅ Enhanced API testing completed!")
    print("\n📝 Check logs/log.jsonl for logged interactions")
    print("💡 Note: First few requests might be slower while the model loads")

if __name__ == "__main__":
    test_api()