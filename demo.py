#!/usr/bin/env python3
"""
Demo script for Networking Tool Copilot
"""

import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.command_processor import CommandProcessor
from core.llm_client import LLMClient
from renderers.terminal_renderer import TerminalRenderer


async def demo_basic_usage():
    """Demo basic usage"""
    print("🌐 Networking Tool Copilot Demo")
    print("=" * 50)
    
    # Initialize
    llm_client = LLMClient()
    processor = CommandProcessor(llm_client)
    renderer = TerminalRenderer()
    
    # Demo commands
    demo_commands = [
        "echo 'Network interface information'",
        "echo 'Ping test to localhost'",
        "echo 'Route analysis example'"
    ]
    
    for i, command in enumerate(demo_commands, 1):
        print(f"\n🔍 Demo {i}: {command}")
        print("=" * 40)
        
        result = await processor.process_command(command)
        renderer.render_result(result, simple=True)
        
        print(f"\n✅ Demo {i} completed")
    
    print("\n" + "=" * 50)
    print("🎉 Demo completed!")


async def demo_with_user_context():
    """Demo with user context"""
    print("\n👤 Demo with User Context")
    print("=" * 50)
    
    llm_client = LLMClient()
    processor = CommandProcessor(llm_client)
    renderer = TerminalRenderer()
    
    # Test with different user levels
    user_contexts = [
        {"user_level": "beginner", "description": "Beginner user"},
        {"user_level": "intermediate", "description": "Intermediate user"},
        {"user_level": "expert", "description": "Expert user"}
    ]
    
    test_command = "echo 'Network command with context'"
    
    for context in user_contexts:
        print(f"\n👤 {context['description']}")
        print("-" * 30)
        
        result = await processor.process_command(test_command, context)
        renderer.render_result(result, simple=(context['user_level'] == 'beginner'))
    
    print("\n✅ User context demo completed!")


def demo_command_validation():
    """Demo command validation"""
    print("\n🔒 Command Validation Demo")
    print("=" * 50)
    
    from core.command_validator import CommandValidator
    
    validator = CommandValidator()
    
    commands_to_test = [
        ("ping google.com", "Valid networking command"),
        ("traceroute 8.8.8.8", "Valid traceroute"),
        ("rm -rf /", "Dangerous command (should be blocked)"),
        ("sudo shutdown", "Special command (should be blocked)"),
        ("ls -la", "Non-networking command (should be blocked)")
    ]
    
    for command, description in commands_to_test:
        print(f"\n🔍 Testing: {description}")
        print(f"Command: {command}")
        
        result = validator.validate_command(command)
        
        if result.valid:
            print("✅ Valid command")
        else:
            print(f"❌ Invalid: {result.error}")
        
        if result.warnings:
            print(f"⚠️  Warnings: {', '.join(result.warnings)}")


def main():
    """Main demo function"""
    print("🚀 Networking Tool Copilot Demo")
    print("=" * 60)
    
    # Demo command validation
    demo_command_validation()
    
    # Demo basic usage
    asyncio.run(demo_basic_usage())
    
    # Demo with user context
    asyncio.run(demo_with_user_context())
    
    print("\n" + "=" * 60)
    print("🎉 Demo completed successfully!")
    print("\n💡 To use the tool:")
    print("   python -m src.cli.main run 'your command'")
    print("   python -m src.cli.main list")
    print("   python -m src.cli.main test")


if __name__ == "__main__":
    main() 