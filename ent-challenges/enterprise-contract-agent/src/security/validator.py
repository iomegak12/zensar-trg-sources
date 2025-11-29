"""
Input Validation for Contract Analysis Agent
Validates and sanitizes user inputs to prevent security issues.
"""

import re
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)


class InputValidator:
    """Validates and sanitizes inputs for security."""
    
    def __init__(self, max_length: int = 50000, max_file_size_mb: int = 10):
        """
        Initialize validator.
        
        Args:
            max_length: Maximum allowed text length
            max_file_size_mb: Maximum file size in MB
        """
        self.max_length = max_length
        self.max_file_size = max_file_size_mb * 1024 * 1024  # Convert to bytes
        
        # Dangerous patterns to detect
        self.dangerous_patterns = [
            r'<script[^>]*>.*?</script>',  # Script tags
            r'javascript:',                  # JavaScript protocol
            r'on\w+\s*=',                   # Event handlers
            r'eval\s*\(',                   # Eval calls
            r'exec\s*\(',                   # Exec calls
        ]
    
    def validate_text_length(self, text: str) -> tuple[bool, Optional[str]]:
        """
        Validate text length.
        
        Returns:
            (is_valid, error_message)
        """
        if not text:
            return False, "Text cannot be empty"
        
        if len(text) > self.max_length:
            return False, f"Text exceeds maximum length of {self.max_length} characters"
        
        return True, None
    
    def validate_user_id(self, user_id: str) -> tuple[bool, Optional[str]]:
        """
        Validate user ID format.
        
        Returns:
            (is_valid, error_message)
        """
        if not user_id:
            return False, "User ID cannot be empty"
        
        # Allow alphanumeric, hyphens, underscores
        if not re.match(r'^[a-zA-Z0-9_-]{1,64}$', user_id):
            return False, "Invalid user ID format"
        
        return True, None
    
    def detect_injection_attempts(self, text: str) -> List[str]:
        """
        Detect potential injection attempts.
        
        Returns:
            List of detected dangerous patterns
        """
        detected = []
        
        for pattern in self.dangerous_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                detected.append(pattern)
        
        return detected
    
    def sanitize_text(self, text: str) -> str:
        """
        Sanitize text by removing potentially dangerous content.
        
        Args:
            text: Text to sanitize
            
        Returns:
            Sanitized text
        """
        sanitized = text
        
        # Remove HTML tags
        sanitized = re.sub(r'<[^>]+>', '', sanitized)
        
        # Remove special characters that could be used for injection
        # Keep alphanumeric, spaces, and common punctuation
        sanitized = re.sub(r'[^\w\s.,;:!?()\[\]{}\-\'\"/@#$%&*+=<>]', '', sanitized)
        
        return sanitized
    
    def validate_file_size(self, file_size: int) -> tuple[bool, Optional[str]]:
        """
        Validate file size.
        
        Args:
            file_size: File size in bytes
            
        Returns:
            (is_valid, error_message)
        """
        if file_size > self.max_file_size:
            max_mb = self.max_file_size / (1024 * 1024)
            return False, f"File size exceeds maximum of {max_mb}MB"
        
        return True, None
    
    def validate_file_type(self, filename: str, allowed_extensions: List[str] = None) -> tuple[bool, Optional[str]]:
        """
        Validate file type by extension.
        
        Args:
            filename: Name of the file
            allowed_extensions: List of allowed extensions (default: ['pdf'])
            
        Returns:
            (is_valid, error_message)
        """
        if allowed_extensions is None:
            allowed_extensions = ['pdf']
        
        if not filename:
            return False, "Filename cannot be empty"
        
        # Extract extension
        if '.' not in filename:
            return False, "File must have an extension"
        
        extension = filename.split('.')[-1].lower()
        
        if extension not in allowed_extensions:
            return False, f"File type .{extension} not allowed. Allowed: {', '.join(allowed_extensions)}"
        
        return True, None
    
    def validate_contract_input(
        self,
        text: str,
        user_id: str,
        file_path: Optional[str] = None
    ) -> tuple[bool, List[str]]:
        """
        Comprehensive validation for contract input.
        
        Returns:
            (is_valid, list_of_errors)
        """
        errors = []
        
        # Validate text length
        valid, error = self.validate_text_length(text)
        if not valid:
            errors.append(error)
        
        # Validate user ID
        valid, error = self.validate_user_id(user_id)
        if not valid:
            errors.append(error)
        
        # Check for injection attempts
        injections = self.detect_injection_attempts(text)
        if injections:
            errors.append(f"Potential injection detected: {len(injections)} suspicious patterns")
            logger.warning(f"Injection attempt detected for user {user_id}")
        
        # Validate file if provided
        if file_path:
            valid, error = self.validate_file_type(file_path)
            if not valid:
                errors.append(error)
        
        is_valid = len(errors) == 0
        
        if not is_valid:
            logger.warning(f"Input validation failed: {errors}")
        
        return is_valid, errors


# Singleton instance
_validator = None


def get_validator() -> InputValidator:
    """Get or create validator instance."""
    global _validator
    if _validator is None:
        import os
        max_length = int(os.getenv("MAX_INPUT_LENGTH", "50000"))
        _validator = InputValidator(max_length=max_length)
    return _validator
