#!/usr/bin/env python3
"""
Test LLM client configuration
"""

import os
import asyncio
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.llm_client import LLMClient, LLMConfig, LLMProvider

async def test_llm():
    print("🔍 Testing LLM Client Configuration...")
    
    # Check environment variables
    print(f"OPENAI_API_KEY: {'Set' if os.getenv('OPENAI_API_KEY') else 'Not set'}")
    print(f"LLM_PROVIDER: {os.getenv('LLM_PROVIDER', 'openai')}")
    
    # Create client
    client = LLMClient()
    print(f"Provider: {client.config.provider}")
    print(f"API Key: {'Set' if client.config.api_key else 'Not set'}")
    print(f"Model: {client.config.model}")
    
    # Test with a simple prompt
    prompt = "Explain this network command output: ping -c 1 127.0.0.1"
    
    print("\n🧪 Testing LLM response...")
    try:
        response = await client.get_explanation(prompt)
        print(f"Response: {response[:200]}...")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_llm()) 