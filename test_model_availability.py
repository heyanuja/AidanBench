#!/usr/bin/env python3
"""
test_model_availability.py

Test which models from model_list.py are actually available via API.
Tests each model with a simple prompt to verify connectivity.
"""
import os
import sys
import json
import time

# Change to the directory containing this script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("Environment variables loaded from .env")
except ImportError:
    print("python-dotenv not available, using system environment variables")

# Add benchmark directory to path
sys.path.append('./benchmark')

from models import chat_with_model

# Models that don't have results yet (from analysis)
MISSING_MODELS = [
    # High priority - likely to work
    "openai/gpt-4o-2024-08-06",
    "openai/gpt-4o-2024-05-13", 
    "openai/gpt-4o-mini-2024-07-18",
    "openai/o1-mini",
    "openai/o1-preview",
    "openai/o1",
    "openai/chatgpt-4o-latest",
    "anthropic/claude-3.5-sonnet",
    "anthropic/claude-3.5-sonnet-20240620",
    "anthropic/claude-3-opus",
    "anthropic/claude-3-sonnet",
    "anthropic/claude-3-haiku",
    "anthropic/claude-3.7-sonnet",
    "anthropic/claude-3.7-sonnet:thinking",
    "meta-llama/llama-3.1-8b-instruct",
    "meta-llama/llama-3.1-70b-instruct", 
    "meta-llama/llama-3.1-405b-instruct",
    "mistralai/mistral-large-latest",
    "deepseek/deepseek-chat",
    
    # Grok 4 variants (newly added)
    "x-ai/grok-4",
    "x-ai/grok-4:low",
    "x-ai/grok-4:medium", 
    "x-ai/grok-4:high",
    "x-ai/grok-4:thinking",
    "x-ai/grok-beta",
    "x-ai/grok-3-mini-beta:low",
    
    # Google models (may not be available)
    "google/gemini-2.0-flash",
    "google/gemini-2.0-flash-exp",
    "google/gemini-2.5-pro-preview-03-25",
    "google/gemini-flash-1.5",
    "google/gemini-pro-1.5",
    
    # Future/questionable models
    "openai/gpt-4.5-preview",
    "anthropic/claude-opus-4",
    "anthropic/claude-sonnet-4",
]

def test_model_availability():
    """Test which models are actually available via API."""
    available = []
    unavailable = []
    test_prompt = "What is 2 + 2?"
    
    print(f"Testing {len(MISSING_MODELS)} models for API availability...")
    print("=" * 60)
    
    for i, model in enumerate(MISSING_MODELS, 1):
        print(f"[{i:2d}/{len(MISSING_MODELS)}] Testing {model}...", end=" ")
        
        try:
            response = chat_with_model(
                prompt=test_prompt,
                model=model,
                max_tokens=50,
                temperature=0
            )
            
            # Basic validation - should get a numeric answer
            if response and len(response.strip()) > 0:
                print("✓ AVAILABLE")
                available.append({
                    "model": model,
                    "status": "available",
                    "response": response.strip()[:100] + "..." if len(response) > 100 else response.strip()
                })
            else:
                print("✗ Empty response")
                unavailable.append({"model": model, "error": "Empty response"})
                
        except Exception as e:
            error_msg = str(e)
            print(f"✗ ERROR: {error_msg[:50]}...")
            unavailable.append({"model": model, "error": error_msg})
        
        # Add delay to avoid rate limiting
        time.sleep(1)
    
    # Results summary
    print("\n" + "=" * 60)
    print(f"SUMMARY: {len(available)} available, {len(unavailable)} unavailable")
    print("=" * 60)
    
    if available:
        print(f"\n✓ AVAILABLE MODELS ({len(available)}):")
        for model_info in available:
            print(f"  - {model_info['model']}")
    
    if unavailable:
        print(f"\n✗ UNAVAILABLE MODELS ({len(unavailable)}):")
        for model_info in unavailable:
            error = model_info['error'][:50] + "..." if len(model_info['error']) > 50 else model_info['error']
            print(f"  - {model_info['model']} ({error})")
    
    # Save detailed results
    results = {
        "test_date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "available": available,
        "unavailable": unavailable,
        "summary": {
            "total_tested": len(MISSING_MODELS),
            "available_count": len(available),
            "unavailable_count": len(unavailable)
        }
    }
    
    with open("model_availability_test.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDetailed results saved to: model_availability_test.json")
    
    if available:
        print(f"\nNext steps:")
        print(f"1. Run benchmark on available models: python fill_missing_results.py --file results.json")
        print(f"2. Estimated cost for {len(available)} models: ~${len(available) * 3-8} (rough estimate)")
    
    return available, unavailable

if __name__ == "__main__":
    test_model_availability()