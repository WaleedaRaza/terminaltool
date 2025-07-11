#!/usr/bin/env python3
"""
Installation script for Networking Tool Copilot
"""

import subprocess
import sys
import os


def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def install_package():
    """Install the package in development mode"""
    print(" Installing package in development mode...")
    
    try:
        subprocess.check_call([sys.executable, "setup.py", "develop"])
        print("✅ Package installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install package: {e}")
        return False


def test_installation():
    """Test the installation"""
    print("🧪 Testing installation...")
    
    try:
        # Test imports
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
        
        from core.command_processor import CommandProcessor
        from core.llm_client import LLMClient
        from core.command_validator import CommandValidator
        
        print("✅ All modules imported successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False


def main():
    """Main installation function"""
    print("🚀 Installing Networking Tool Copilot")
    print("=" * 50)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Installation failed at dependencies step!")
        return
    
    # Install package
    if not install_package():
        print("\n❌ Installation failed at package step!")
        return
    
    # Test installation
    if not test_installation():
        print("\n❌ Installation test failed!")
        return
    
    print("\n🎉 Installation completed successfully!")
    print("\n💡 You can now use:")
    print("   python run_test.py")
    print("   python demo.py")
    print("   python -m src.cli.main run 'your command'")


if __name__ == "__main__":
    main()