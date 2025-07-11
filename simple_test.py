#!/usr/bin/env python3
"""
Simple test for Networking Tool Copilot
"""

import sys
import os
import asyncio

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

async def main():
    """Simple test"""
    print("🚀 Testing Networking Tool Copilot")
    print("=" * 40)
    
    try:
        # Import modules
        from core.command_processor import CommandProcessor
        from core.llm_client import LLMClient
        from renderers.terminal_renderer import TerminalRenderer
        
        print("✅ All modules imported successfully!")
        
        # Initialize components
        llm_client = LLMClient()
        processor = CommandProcessor(llm_client)
        renderer = TerminalRenderer()
        
        print("✅ Components initialized!")
        
        # Test a networking command
        result = await processor.process_command("ping -c 1 127.0.0.1")
        print(f"✅ Command processed: {result.status.value}")
        
        # Render the result
        renderer.render_result(result, simple=True)
        
        print("\n🎉 Networking Tool Copilot is working!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 