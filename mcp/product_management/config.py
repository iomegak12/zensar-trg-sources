"""
Configuration management for Product Management Library.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for the Products Library."""
    
    def __init__(self):
        """Initialize configuration from environment variables."""
        self.database_path = os.getenv('DATABASE_PATH', 'dbs/products.db')
        self.environment = os.getenv('ENVIRONMENT', 'development')
        self.api_name = os.getenv('API_NAME', 'Products Library')
        self.api_description = os.getenv('API_DESCRIPTION', 
                                        'Python library for managing product information')
    
    def get_database_path(self) -> str:
        """Get the database path."""
        return self.database_path
    
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == 'production'
    
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment.lower() == 'development'


# Global config instance
config = Config()
