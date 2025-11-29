"""
Rate Limiter for Contract Analysis Agent
Implements token bucket algorithm for rate limiting.
"""

import time
from collections import defaultdict
from threading import Lock
from typing import Optional
import logging
import os

logger = logging.getLogger(__name__)


class TokenBucket:
    """Token bucket for rate limiting."""
    
    def __init__(self, capacity: int, refill_rate: float):
        """
        Initialize token bucket.
        
        Args:
            capacity: Maximum number of tokens
            refill_rate: Tokens added per second
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.time()
        self.lock = Lock()
    
    def consume(self, tokens: int = 1) -> bool:
        """
        Try to consume tokens.
        
        Args:
            tokens: Number of tokens to consume
            
        Returns:
            True if tokens were consumed, False if insufficient tokens
        """
        with self.lock:
            # Refill tokens based on time passed
            now = time.time()
            time_passed = now - self.last_refill
            tokens_to_add = time_passed * self.refill_rate
            
            self.tokens = min(self.capacity, self.tokens + tokens_to_add)
            self.last_refill = now
            
            # Check if we have enough tokens
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            
            return False
    
    def get_available_tokens(self) -> float:
        """Get current number of available tokens."""
        with self.lock:
            now = time.time()
            time_passed = now - self.last_refill
            tokens_to_add = time_passed * self.refill_rate
            return min(self.capacity, self.tokens + tokens_to_add)


class RateLimiter:
    """Rate limiter using token bucket algorithm."""
    
    def __init__(
        self,
        requests_per_period: int = 10,
        period_seconds: int = 60,
        burst_capacity: Optional[int] = None
    ):
        """
        Initialize rate limiter.
        
        Args:
            requests_per_period: Number of requests allowed per period
            period_seconds: Length of period in seconds
            burst_capacity: Optional burst capacity (default: requests_per_period * 2)
        """
        self.requests_per_period = requests_per_period
        self.period_seconds = period_seconds
        
        # Calculate refill rate (tokens per second)
        self.refill_rate = requests_per_period / period_seconds
        
        # Burst capacity allows temporary spike above normal rate
        self.burst_capacity = burst_capacity or (requests_per_period * 2)
        
        # Token buckets per user
        self.buckets: dict[str, TokenBucket] = defaultdict(
            lambda: TokenBucket(self.burst_capacity, self.refill_rate)
        )
        
        logger.info(
            f"Rate limiter initialized: {requests_per_period} requests per {period_seconds}s "
            f"(burst: {self.burst_capacity})"
        )
    
    def allow_request(self, user_id: str, tokens: int = 1) -> tuple[bool, Optional[str]]:
        """
        Check if request is allowed for user.
        
        Args:
            user_id: User identifier
            tokens: Number of tokens to consume (default: 1)
            
        Returns:
            (is_allowed, error_message)
        """
        bucket = self.buckets[user_id]
        
        if bucket.consume(tokens):
            logger.debug(f"Request allowed for user {user_id}")
            return True, None
        
        # Calculate wait time
        available = bucket.get_available_tokens()
        needed = tokens - available
        wait_seconds = needed / self.refill_rate
        
        error_msg = f"Rate limit exceeded. Try again in {wait_seconds:.1f} seconds"
        logger.warning(f"Rate limit exceeded for user {user_id}")
        
        return False, error_msg
    
    def get_user_status(self, user_id: str) -> dict:
        """
        Get rate limit status for user.
        
        Args:
            user_id: User identifier
            
        Returns:
            Dict with status information
        """
        bucket = self.buckets.get(user_id)
        
        if not bucket:
            return {
                "available_tokens": self.burst_capacity,
                "capacity": self.burst_capacity,
                "refill_rate": self.refill_rate,
                "utilization": 0.0
            }
        
        available = bucket.get_available_tokens()
        
        return {
            "available_tokens": available,
            "capacity": self.burst_capacity,
            "refill_rate": self.refill_rate,
            "utilization": (self.burst_capacity - available) / self.burst_capacity
        }
    
    def reset_user(self, user_id: str):
        """Reset rate limit for a user."""
        if user_id in self.buckets:
            del self.buckets[user_id]
            logger.info(f"Rate limit reset for user {user_id}")


# Singleton instance
_rate_limiter = None


def get_rate_limiter() -> RateLimiter:
    """Get or create rate limiter instance."""
    global _rate_limiter
    if _rate_limiter is None:
        requests = int(os.getenv("RATE_LIMIT_REQUESTS", "10"))
        period = int(os.getenv("RATE_LIMIT_PERIOD", "60"))
        _rate_limiter = RateLimiter(
            requests_per_period=requests,
            period_seconds=period
        )
    return _rate_limiter


def rate_limit_check(user_id: str, tokens: int = 1) -> tuple[bool, Optional[str]]:
    """
    Convenience function to check rate limit.
    
    Args:
        user_id: User identifier
        tokens: Number of tokens to consume
        
    Returns:
        (is_allowed, error_message)
    """
    limiter = get_rate_limiter()
    return limiter.allow_request(user_id, tokens)
