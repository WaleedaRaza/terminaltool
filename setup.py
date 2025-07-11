#!/usr/bin/env python3
"""
Setup script for Networking Tool Copilot
"""

from config import setup_config, set_api_key, get_api_key

def main():
    print("🚀 Networking Tool Copilot Setup")
    print("=" * 40)
    
    # Check if API key is already set
    current_key = get_api_key()
    if current_key:
        print(f"✅ API key is already configured: {current_key[:20]}...")
        change = input("Do you want to change it? (y/n): ").lower().strip()
        if change != 'y':
            print("Setup complete!")
            return
    
    # Get API key
    print("\n🔑 OpenAI API Key Setup")
    print("You need an OpenAI API key to use the AI analysis features.")
    print("Get one at: https://platform.openai.com/api-keys")
    print()
    
    api_key = input("Enter your OpenAI API key: ").strip()
    if not api_key:
        print("❌ No API key provided. Setup incomplete.")
        return
    
    # Save the API key
    if set_api_key(api_key):
        print("✅ API key saved successfully!")
        print("You can now run the web server without setting environment variables.")
    else:
        print("❌ Failed to save API key.")
        return
    
    print("\n🎉 Setup complete!")
    print("Run 'python3 simple_web.py' to start the server.")

if __name__ == "__main__":
    main() 