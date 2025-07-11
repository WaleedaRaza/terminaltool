#!/usr/bin/env python3
"""
Test script for web server
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from web.server import create_app
    print("✅ Import successful")
    
    app = create_app()
    print("✅ App created successfully")
    
    print("✅ Web server is ready!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc() 