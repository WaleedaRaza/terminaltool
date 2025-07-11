#!/usr/bin/env python3
"""
Example usage of Networking Tool Copilot
"""

import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.command_processor import CommandProcessor
from core.llm_client import LLMClient
from renderers.terminal_renderer import TerminalRenderer


async def example_basic_usage():
    """Example of basic usage"""
    print("🌐 Networking Tool Copilot - Basic Usage Example")
    print("=" * 60)
    
    # Initialize components
    llm_client = LLMClient()
    processor = CommandProcessor(llm_client)
    renderer = TerminalRenderer()
    
    # Example 1: Simple command
    print("\n📋 Example 1: Simple command")
    print("-" * 40)
    
    command = "echo 'Testing network comm 