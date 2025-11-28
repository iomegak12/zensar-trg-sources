#!/usr/bin/env python3
"""
Production startup script for Agentic RAG API
"""
import os
import sys
import argparse

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def start_server(host="0.0.0.0", port=None, workers=1, reload=False):
    """Start the FastAPI server with uvicorn"""
    import uvicorn
    from src.agentic_rag.config import Config
    
    # Load config to get default port
    config = Config()
    if port is None:
        port = config.api_port
    
    print(f"🚀 Starting Agentic RAG API server...")
    print(f"📍 Host: {host}")
    print(f"📍 Port: {port}")
    print(f"📍 Workers: {workers}")
    print(f"📍 Reload: {reload}")
    print(f"📍 Environment: {config.environment}")
    print()
    
    # Start the server
    uvicorn.run(
        "api.main:app",
        host=host,
        port=port,
        workers=workers,
        reload=reload,
        log_level="info"
    )

def main():
    parser = argparse.ArgumentParser(description="Start Agentic RAG API server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, help="Port to bind to (default from .env)")
    parser.add_argument("--workers", type=int, default=1, help="Number of worker processes")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload for development")
    
    args = parser.parse_args()
    
    start_server(
        host=args.host,
        port=args.port,
        workers=args.workers,
        reload=args.reload
    )

if __name__ == "__main__":
    main()