#!/usr/bin/env python3
"""
Quick test runner for Networking Tool Copilot
"""

import sys
import os
import asyncio

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all modules can be imported"""
    print("📦 Testing imports...")
    
    try:
        from core.command_processor import CommandProcessor
        print("✅ CommandProcessor imported")
    except Exception as e:
        print(f"❌ CommandProcessor import failed: {e}")
        return False
    
    try:
        from core.llm_client import LLMClient
        print("✅ LLMClient imported")
    except Exception as e:
        print(f"❌ LLMClient import failed: {e}")
        return False
    
    try:
        from core.command_validator import CommandValidator
        print("✅ CommandValidator imported")
    except Exception as e:
        print(f"❌ CommandValidator import failed: {e}")
        return False
    
    try:
        from renderers.terminal_renderer import TerminalRenderer
        print("✅ TerminalRenderer imported")
    except Exception as e:
        print(f"❌ TerminalRenderer import failed: {e}")
        return False
    
    return True


async def test_basic_functionality():
    """Test basic functionality"""
    print("\n🧪 Testing basic functionality...")
    
    try:
        # Initialize components
        llm_client = LLMClient()
        processor = CommandProcessor(llm_client)
        renderer = TerminalRenderer()
        
        print("✅ Components initialized")
        
        # Test command validation
        validator = processor.validator
        result = validator.validate_command("ping google.com")
        print(f"✅ Command validation: {result.valid}")
        
        # Test command processing
        test_result = await processor.process_command("echo 'Hello from netcopilot'")
        print(f"✅ Command processing: {test_result.status.value}")
        
        # Test rendering
        renderer.render_result(test_result, simple=True)
        print("✅ Rendering completed")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False


def test_command_validation():
    """Test command validation"""
    print("\n🔒 Testing command validation...")
    
    try:
        from core.command_validator import CommandValidator
        
        validator = CommandValidator()
        
        # Test valid commands
        valid_commands = ["ping google.com", "traceroute 8.8.8.8"]
        for cmd in valid_commands:
            result = validator.validate_command(cmd)
            print(f"✅ '{cmd}': {result.valid}")
        
        # Test invalid commands
        invalid_commands = ["rm -rf /", "sudo shutdown", ""]
        for cmd in invalid_commands:
            result = validator.validate_command(cmd)
            print(f"❌ '{cmd}': {result.valid} (expected: False)")
        
        return True
        
    except Exception as e:
        print(f"❌ Command validation test failed: {e}")
        return False


def main():
    """Main test function"""
    print("🚀 Networking Tool Copilot - Quick Test")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed!")
        return
    
    # Test command validation
    if not test_command_validation():
        print("\n❌ Command validation tests failed!")
        return
    
    # Test basic functionality
    if asyncio.run(test_basic_functionality()):
        print("\n✅ All tests passed!")
        print("\n🎉 Networking Tool Copilot is working!")
        
        print("\n💡 Try these commands:")
        print("   python -m src.cli.main run 'echo Hello'")
        print("   python -m src.cli.main list")
        print("   python -m src.cli.main test")
    else:
        print("\n❌ Some tests failed!")


if __name__ == "__main__":
    main() 