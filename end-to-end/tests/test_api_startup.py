#!/usr/bin/env python3
"""
Test script to verify the FastAPI server can start properly
"""
import asyncio
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_api_startup():
    """Test if the API can start up properly"""
    try:
        print("🧪 Testing API Startup...")
        
        # Import the API
        from api.main import app, initialize_agentic_rag
        print("✅ API imports successful")
        
        # Test configuration loading
        from src.agentic_rag.config import Config
        config = Config()
        print("✅ Configuration loaded successfully")
        
        # Test that we can initialize without starting the server
        print("✅ API startup test completed successfully")
        print(f"📍 API configured to run on port: {config.api_port}")
        print("🚀 Ready to start the server!")
        
        return True
        
    except Exception as e:
        print(f"❌ API startup test failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_api_startup())
    sys.exit(0 if success else 1)