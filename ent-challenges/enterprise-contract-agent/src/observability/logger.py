"""
Structured Logging Configuration for Contract Analysis Agent
Provides centralized, structured logging with log levels and formatting.
"""

import logging
import json
import sys
from datetime import datetime
from typing import Any, Dict
import os


class StructuredFormatter(logging.Formatter):
    """Custom formatter that outputs structured JSON logs."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Add extra fields if present
        if hasattr(record, 'request_id'):
            log_data['request_id'] = record.request_id
        
        if hasattr(record, 'user_id'):
            log_data['user_id'] = record.user_id
        
        if hasattr(record, 'contract_type'):
            log_data['contract_type'] = record.contract_type
        
        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)


class ContractAgentLogger:
    """Centralized logger for the contract analysis agent."""
    
    def __init__(self, name: str = "contract-agent"):
        """
        Initialize the logger.
        
        Args:
            name: Logger name
        """
        self.logger = logging.getLogger(name)
        self._request_context = {}  # Store request-level context
        self._setup_logger()
    
    def _setup_logger(self):
        """Configure logger with appropriate handlers and formatters."""
        # Get log level from environment
        log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        self.logger.setLevel(getattr(logging, log_level))
        
        # Remove existing handlers
        self.logger.handlers.clear()
        
        # Console handler with structured format
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        
        # Use JSON format for production, readable format for development
        if os.getenv("ENVIRONMENT", "development") == "production":
            console_handler.setFormatter(StructuredFormatter())
        else:
            # Readable format for development
            format_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            console_handler.setFormatter(logging.Formatter(format_str))
        
        self.logger.addHandler(console_handler)
        
        # File handler (optional)
        log_file = os.getenv("LOG_FILE")
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(StructuredFormatter())
            self.logger.addHandler(file_handler)
    
    def set_request_context(self, **context):
        """
        Set request-level context that will be included in all subsequent log entries.
        
        Args:
            **context: Key-value pairs to include in logs (e.g., request_id, user_id, session_id)
        """
        self._request_context.update(context)
    
    def clear_request_context(self):
        """Clear all request-level context."""
        self._request_context.clear()
    
    def _merge_context(self, kwargs):
        """Merge request context with log-specific kwargs."""
        merged = self._request_context.copy()
        merged.update(kwargs)
        return merged
    
    def debug(self, message: str, **kwargs):
        """Log debug message with optional context."""
        self.logger.debug(message, extra=self._merge_context(kwargs))
    
    def info(self, message: str, **kwargs):
        """Log info message with optional context."""
        self.logger.info(message, extra=self._merge_context(kwargs))
    
    def warning(self, message: str, **kwargs):
        """Log warning message with optional context."""
        self.logger.warning(message, extra=self._merge_context(kwargs))
    
    def error(self, message: str, exc_info=None, **kwargs):
        """Log error message with optional exception info."""
        self.logger.error(message, exc_info=exc_info, extra=self._merge_context(kwargs))
    
    def critical(self, message: str, exc_info=None, **kwargs):
        """Log critical message with optional exception info."""
        self.logger.critical(message, exc_info=exc_info, extra=self._merge_context(kwargs))
    
    def log_request(self, request_id: str, user_id: str, contract_type: str, message: str):
        """Log with request context."""
        self.info(
            message,
            request_id=request_id,
            user_id=user_id,
            contract_type=contract_type
        )
    
    def log_security_event(self, event_type: str, severity: str, details: Dict[str, Any]):
        """Log security-related events."""
        self.warning(
            f"Security event: {event_type}",
            event_type=event_type,
            severity=severity,
            **details
        )
    
    def log_compliance_event(self, check_type: str, result: str, details: Dict[str, Any]):
        """Log compliance-related events."""
        self.info(
            f"Compliance check: {check_type} - {result}",
            check_type=check_type,
            result=result,
            **details
        )


# Global logger instance
logger = ContractAgentLogger()


def get_logger(name: str = None) -> ContractAgentLogger:
    """Get logger instance."""
    if name:
        return ContractAgentLogger(name)
    return logger
