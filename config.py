#!/usr/bin/env python3
"""
Configuration file for Networking Tool Copilot
"""

import os
from pathlib import Path

# Default configuration
DEFAULT_CONFIG = {
    "openai_api_key": "",
    "llm_provider": "openai",
    "llm_model": "gpt-4",
    "llm_temperature": 0.3,
    "llm_max_tokens": 1000,
    "llm_timeout": 30,
    "web_port": 3000,
    "web_host": "127.0.0.1"
}

CONFIG_FILE = Path("netcopilot_config.json")

def load_config():
    """Load configuration from file or create default"""
    import json
    
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                # Merge with defaults for any missing keys
                for key, value in DEFAULT_CONFIG.items():
                    if key not in config:
                        config[key] = value
                return config
        except Exception as e:
            print(f"Error loading config: {e}")
            return DEFAULT_CONFIG.copy()
    else:
        # Create default config file
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()

def save_config(config):
    """Save configuration to file"""
    import json
    
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False

def set_api_key(api_key):
    """Set the OpenAI API key"""
    config = load_config()
    config["openai_api_key"] = api_key
    return save_config(config)

def get_api_key():
    """Get the OpenAI API key"""
    config = load_config()
    return config.get("openai_api_key", "")

def setup_config():
    """Interactive setup for configuration"""
    print("🔧 Networking Tool Copilot Configuration")
    print("=" * 40)
    
    config = load_config()
    
    # Get API key
    current_key = config.get("openai_api_key", "")
    if current_key:
        print(f"Current API key: {current_key[:20]}...")
        change = input("Change API key? (y/n): ").lower().strip()
        if change == 'y':
            api_key = input("Enter your OpenAI API key: ").strip()
            if api_key:
                config["openai_api_key"] = api_key
    else:
        api_key = input("Enter your OpenAI API key: ").strip()
        if api_key:
            config["openai_api_key"] = api_key
    
    # Save config
    if save_config(config):
        print("✅ Configuration saved successfully!")
        print(f"Config file: {CONFIG_FILE.absolute()}")
    else:
        print("❌ Failed to save configuration")

if __name__ == "__main__":
    setup_config() 