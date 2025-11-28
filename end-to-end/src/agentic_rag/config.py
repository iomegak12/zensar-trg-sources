import os
from typing import List
from dotenv import load_dotenv
from .prompts import DefaultConfig


class Config:
    """Configuration management for Agentic RAG system."""
    
    def __init__(self):
        print("Loading .env file...")
        load_dotenv()
        print(f"✓ .env loaded from current directory")
        
        # Azure OpenAI Configuration
        self.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.azure_deployment = os.getenv("AZURE_DEPLOYMENT_NAME")
        self.azure_api_version = os.getenv("AZURE_API_VERSION")
        self.azure_embedding_deployment = os.getenv("AZURE_EMBEDDING_DEPLOYMENT", "text-embedding-3-large")
        
        print(f"Azure endpoint: {self.azure_endpoint[:50]}..." if self.azure_endpoint else "Azure endpoint: NOT SET")
        
        # Google Search Configuration
        self.google_serper_api_key = os.getenv("GOOGLE_SERPER_API_KEY")
        
        # Vector Store Configuration
        self.vector_store_urls_file = os.getenv("VECTOR_STORE_URLS_FILE", "urls.txt")
        self.default_urls_fallback = os.getenv("DEFAULT_URLS_FALLBACK", "true").lower() == "true"
        
        # User Agent for Web Scraping
        self.user_agent = os.getenv("USER_AGENT", "AgenticRAG/1.0 (Educational Research Tool)")
        
        # Set USER_AGENT environment variable if not already set
        if not os.getenv("USER_AGENT"):
            os.environ["USER_AGENT"] = self.user_agent
        
        # API Configuration
        self.api_port = int(os.getenv("API_PORT", "50000"))
        self.environment = os.getenv("ENVIRONMENT", "production")
        
        # Rate Limiting Configuration
        self.rate_limit_enabled = os.getenv("RATE_LIMIT_ENABLED", "false").lower() == "true"
        self.rate_limit = os.getenv("RATE_LIMIT", "100/minute")
        
        # CORS Configuration
        self.cors_enabled = os.getenv("CORS_ENABLED", "true").lower() == "true"
        cors_origins_str = os.getenv("CORS_ORIGINS", "*")
        self.cors_origins = [origin.strip() for origin in cors_origins_str.split(",")] if cors_origins_str != "*" else ["*"]
        
        # Logging Configuration
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        
        # Validate required configuration
        self._validate()
    
    def _validate(self):
        """Validate that all required configuration is present."""
        required_vars = [
            ("AZURE_OPENAI_ENDPOINT", self.azure_endpoint),
            ("AZURE_OPENAI_API_KEY", self.azure_api_key),
            ("AZURE_DEPLOYMENT_NAME", self.azure_deployment),
            ("AZURE_API_VERSION", self.azure_api_version),
        ]
        
        missing_vars = [var_name for var_name, var_value in required_vars if not var_value]
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        if not self.google_serper_api_key:
            print("Warning: GOOGLE_SERPER_API_KEY not set. Google Search tool will not work.")
    
    def get_vector_store_urls(self) -> List[str]:
        """Load URLs from the configured URLs file."""
        urls = []
        
        if not os.path.exists(self.vector_store_urls_file):
            print(f"Warning: URLs file '{self.vector_store_urls_file}' not found.")
            if self.default_urls_fallback:
                print("Using default URLs from configuration.")
                return DefaultConfig.DEFAULT_URLS
            else:
                raise FileNotFoundError(f"URLs file '{self.vector_store_urls_file}' not found and fallback disabled.")
        
        try:
            with open(self.vector_store_urls_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):  # Skip empty lines and comments
                        urls.append(line)
            
            if not urls:
                print("Warning: No valid URLs found in URLs file.")
                if self.default_urls_fallback:
                    print("Using default URLs from configuration.")
                    return DefaultConfig.DEFAULT_URLS
                else:
                    raise ValueError("No valid URLs found and fallback disabled.")
            
            return urls
            
        except Exception as e:
            print(f"Error reading URLs file: {e}.")
            if self.default_urls_fallback:
                print("Using default URLs from configuration.")
                return DefaultConfig.DEFAULT_URLS
            else:
                raise e