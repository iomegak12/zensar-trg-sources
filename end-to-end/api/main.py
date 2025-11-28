"""
FastAPI REST API for Agentic RAG System
"""
import os
import logging
import time
from contextlib import asynccontextmanager
from typing import Dict, Any, Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel
import colorama
from colorama import Fore, Style, Back

# Initialize colorama for Windows support
colorama.init(autoreset=True)

# Import our AgenticRAG system
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.agentic_rag import AgenticRAG
from src.agentic_rag.config import Config

# Global variables
agentic_rag: Optional[AgenticRAG] = None
config: Optional[Config] = None
logger = logging.getLogger("agentic_rag_api")

# Rate limiter setup
limiter = Limiter(key_func=get_remote_address)

def setup_logging():
    """Setup colorful console logging"""
    # Create custom formatter with colors
    class ColoredFormatter(logging.Formatter):
        COLORS = {
            'DEBUG': Fore.CYAN,
            'INFO': Fore.GREEN,
            'WARNING': Fore.YELLOW,
            'ERROR': Fore.RED,
            'CRITICAL': Fore.RED + Back.YELLOW
        }

        def format(self, record):
            log_color = self.COLORS.get(record.levelname, '')
            record.levelname = f"{log_color}{record.levelname}{Style.RESET_ALL}"
            record.name = f"{Fore.BLUE}{record.name}{Style.RESET_ALL}"
            return super().format(record)

    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )
    
    # Apply colored formatter to all handlers
    for handler in logging.getLogger().handlers:
        handler.setFormatter(ColoredFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))

def print_startup_banner():
    """Print colorful startup banner with configuration"""
    print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{Back.BLACK}   🚀 AGENTIC RAG API SERVER STARTING   {Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}📋 Configuration:{Style.RESET_ALL}")
    print(f"  {Fore.BLUE}API Name:{Style.RESET_ALL} Agentic RAG")
    print(f"  {Fore.BLUE}Version:{Style.RESET_ALL} 1.0")
    print(f"  {Fore.BLUE}Port:{Style.RESET_ALL} {config.api_port}")
    print(f"  {Fore.BLUE}Environment:{Style.RESET_ALL} {config.environment}")
    
    print(f"\n{Fore.YELLOW}🔧 Features:{Style.RESET_ALL}")
    print(f"  {Fore.BLUE}Rate Limiting:{Style.RESET_ALL} {'✅ Enabled' if config.rate_limit_enabled else '❌ Disabled'}")
    if config.rate_limit_enabled:
        print(f"  {Fore.BLUE}Rate Limit:{Style.RESET_ALL} {config.rate_limit}")
    print(f"  {Fore.BLUE}CORS:{Style.RESET_ALL} {'✅ Enabled' if config.cors_enabled else '❌ Disabled'}")
    if config.cors_enabled:
        origins = config.cors_origins if config.cors_origins != ["*"] else ["All Origins (*)"]
        print(f"  {Fore.BLUE}CORS Origins:{Style.RESET_ALL} {', '.join(origins)}")
    
    print(f"\n{Fore.YELLOW}🤖 Azure OpenAI:{Style.RESET_ALL}")
    print(f"  {Fore.BLUE}Endpoint:{Style.RESET_ALL} {config.azure_endpoint}")
    print(f"  {Fore.BLUE}Model:{Style.RESET_ALL} {config.azure_deployment}")
    print(f"  {Fore.BLUE}API Version:{Style.RESET_ALL} {config.azure_api_version}")
    
    print(f"\n{Fore.YELLOW}📚 Vector Store:{Style.RESET_ALL}")
    urls = config.get_vector_store_urls()
    print(f"  {Fore.BLUE}URLs Count:{Style.RESET_ALL} {len(urls)}")
    for i, url in enumerate(urls[:3], 1):  # Show first 3 URLs
        print(f"  {Fore.BLUE}URL {i}:{Style.RESET_ALL} {url}")
    if len(urls) > 3:
        print(f"  {Fore.BLUE}...{Style.RESET_ALL} and {len(urls) - 3} more")
    
    print(f"\n{Fore.YELLOW}🌐 Endpoints:{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}Health:{Style.RESET_ALL} http://localhost:{config.api_port}/health")
    print(f"  {Fore.GREEN}Metrics:{Style.RESET_ALL} http://localhost:{config.api_port}/metrics")
    print(f"  {Fore.GREEN}API Docs:{Style.RESET_ALL} http://localhost:{config.api_port}/docs")
    print(f"  {Fore.GREEN}Query:{Style.RESET_ALL} http://localhost:{config.api_port}/query")
    print(f"  {Fore.GREEN}Refresh:{Style.RESET_ALL} http://localhost:{config.api_port}/refresh")
    
    print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")

async def initialize_agentic_rag():
    """Initialize the AgenticRAG system"""
    global agentic_rag, config
    
    try:
        logger.info("🔧 Loading configuration...")
        config = Config()
        
        setup_logging()
        print_startup_banner()
        
        logger.info("🤖 Initializing Agentic RAG system...")
        start_time = time.time()
        
        # AgenticRAG loads its own config internally
        agentic_rag = AgenticRAG()
        
        init_time = time.time() - start_time
        logger.info(f"✅ Agentic RAG system initialized successfully in {init_time:.2f}s")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize Agentic RAG system: {e}")
        raise

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    await initialize_agentic_rag()
    yield
    # Shutdown
    logger.info("🛑 Shutting down Agentic RAG API server")

# Create FastAPI app
app = FastAPI(
    title="Agentic RAG API",
    description="This Agentic RAG supports enterprise system RAG design with best practices",
    version="1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Add rate limiting error handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add CORS middleware
@app.on_event("startup")
async def setup_cors():
    if config and config.cors_enabled:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=config.cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        logger.info(f"🌐 CORS enabled for origins: {config.cors_origins}")

# Add Prometheus metrics
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

# Mount static files
app.mount("/static", StaticFiles(directory="ui/static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="ui/templates")

# Pydantic models
class QueryRequest(BaseModel):
    question: str
    
    class Config:
        schema_extra = {
            "example": {
                "question": "What is machine learning?"
            }
        }

class QueryResponse(BaseModel):
    answer: str
    metadata: Dict[str, Any]
    processing_time: float

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    agentic_rag_ready: bool

class RefreshResponse(BaseModel):
    status: str
    message: str
    processing_time: float

# Dependency to get rate limit based on config
def get_rate_limit():
    if config and config.rate_limit_enabled:
        return config.rate_limit
    return "1000/minute"  # Very high limit when disabled

# API Endpoints
@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
        version="1.0",
        agentic_rag_ready=agentic_rag is not None
    )

@app.post("/query", response_model=QueryResponse, tags=["RAG"])
@limiter.limit(get_rate_limit())
async def query_agentic_rag(request: Request, query_request: QueryRequest):
    """Query the Agentic RAG system"""
    if not agentic_rag:
        raise HTTPException(status_code=503, detail="Agentic RAG system not initialized")
    
    try:
        start_time = time.time()
        logger.info(f"📝 Processing query: {query_request.question[:100]}...")
        
        result = agentic_rag.query(query_request.question)
        
        processing_time = time.time() - start_time
        logger.info(f"✅ Query processed successfully in {processing_time:.2f}s")
        
        return QueryResponse(
            answer=result.get("answer", "No answer generated"),
            metadata=result.get("metadata", {}),
            processing_time=processing_time
        )
    
    except Exception as e:
        logger.error(f"❌ Error processing query: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.post("/refresh", response_model=RefreshResponse, tags=["Management"])
async def refresh_vector_store(request: Request):
    """Refresh the vector store by reinitializing it"""
    global agentic_rag
    
    try:
        start_time = time.time()
        logger.info("🔄 Refreshing vector store...")
        
        if agentic_rag:
            # Reinitialize the AgenticRAG system
            agentic_rag = AgenticRAG()
            processing_time = time.time() - start_time
            
            logger.info(f"✅ Vector store refreshed successfully in {processing_time:.2f}s")
            
            return RefreshResponse(
                status="success",
                message="Vector store refreshed successfully",
                processing_time=processing_time
            )
        else:
            raise HTTPException(status_code=503, detail="Agentic RAG system not initialized")
            
    except Exception as e:
        logger.error(f"❌ Error refreshing vector store: {e}")
        raise HTTPException(status_code=500, detail=f"Error refreshing vector store: {str(e)}")

@app.get("/", tags=["Info"])
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Agentic RAG API",
        "description": "This Agentic RAG supports enterprise system RAG design with best practices",
        "version": "1.0",
        "docs": "/docs",
        "health": "/health",
        "metrics": "/metrics",
        "ui": "/ui"
    }

# UI Routes
@app.get("/ui", response_class=HTMLResponse, tags=["UI"])
async def ui_home(request: Request):
    """Serve the main UI homepage"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/ui/about", response_class=HTMLResponse, tags=["UI"])
async def ui_about(request: Request):
    """Serve the about page"""
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/ui/contact", response_class=HTMLResponse, tags=["UI"])
async def ui_contact(request: Request):
    """Serve the contact page"""
    return templates.TemplateResponse("contact.html", {"request": request})

@app.get("/ui/chat", response_class=HTMLResponse, tags=["UI"])
async def ui_chat(request: Request):
    """Serve the chat interface"""
    return templates.TemplateResponse("chat.html", {"request": request})

if __name__ == "__main__":
    # Load configuration
    config = Config()
    
    # Run the server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=config.api_port,
        reload=config.environment == "development",
        log_level="info"
    )