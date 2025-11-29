"""
Prometheus Metrics Collection for Contract Analysis Agent
Tracks key performance indicators and business metrics.
"""

from prometheus_client import Counter, Histogram, Gauge, Info
from prometheus_client import start_http_server
from functools import wraps
from contextlib import contextmanager
import time
import os
import logging

logger = logging.getLogger(__name__)


# Define metrics
CONTRACT_ANALYSIS_REQUESTS = Counter(
    'contract_analysis_requests_total',
    'Total number of contract analysis requests',
    ['contract_type', 'status']
)

CONTRACT_ANALYSIS_DURATION = Histogram(
    'contract_analysis_duration_seconds',
    'Time spent analyzing contracts',
    ['contract_type', 'complexity'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0]
)

LLM_TOKEN_USAGE = Counter(
    'llm_token_usage_total',
    'Total number of LLM tokens used',
    ['operation', 'model']
)

PII_DETECTIONS = Counter(
    'pii_detections_total',
    'Number of PII entities detected',
    ['entity_type']
)

SECURITY_VIOLATIONS = Counter(
    'security_violations_total',
    'Security policy violations',
    ['violation_type']
)

COMPLIANCE_CHECKS = Counter(
    'compliance_checks_total',
    'Compliance check results',
    ['check_type', 'result']
)

ACTIVE_REQUESTS = Gauge(
    'contract_analysis_active_requests',
    'Number of currently active analysis requests'
)

ERROR_RATE = Counter(
    'contract_analysis_errors_total',
    'Total number of errors',
    ['error_type', 'component']
)


class MetricsCollector:
    """Collects and exposes Prometheus metrics."""
    
    def __init__(self):
        """Initialize metrics collector."""
        self.enabled = os.getenv("ENABLE_OBSERVABILITY", "true").lower() == "true"
        self.port = int(os.getenv("PROMETHEUS_PORT", "8000"))
        
        if self.enabled:
            self._start_metrics_server()
    
    def _start_metrics_server(self):
        """Start Prometheus metrics HTTP server."""
        try:
            start_http_server(self.port)
            logger.info(f"✅ Prometheus metrics server started on port {self.port}")
            logger.info(f"   Metrics available at: http://localhost:{self.port}/metrics")
        except Exception as e:
            logger.error(f"Failed to start metrics server: {e}")
            self.enabled = False
    
    def record_request(self, contract_type: str, status: str):
        """Record a contract analysis request."""
        if self.enabled:
            CONTRACT_ANALYSIS_REQUESTS.labels(
                contract_type=contract_type,
                status=status
            ).inc()
    
    def record_duration(self, operation: str = None, contract_type: str = "unknown", 
                       complexity: str = "unknown", duration: float = 0.0):
        """Record analysis duration."""
        if self.enabled:
            # Support both old signature (contract_type, complexity, duration)
            # and new signature (operation=X, duration=Y)
            actual_type = contract_type
            actual_complexity = complexity
            
            CONTRACT_ANALYSIS_DURATION.labels(
                contract_type=actual_type,
                complexity=actual_complexity
            ).observe(duration)
    
    def record_tokens(self, operation: str, model: str, token_count: int):
        """Record LLM token usage."""
        if self.enabled:
            LLM_TOKEN_USAGE.labels(
                operation=operation,
                model=model
            ).inc(token_count)
    
    def record_llm_tokens(self, model: str, operation: str, tokens: int):
        """Record LLM token usage (alias with notebook-friendly signature)."""
        if self.enabled:
            LLM_TOKEN_USAGE.labels(
                operation=operation,
                model=model
            ).inc(tokens)
    
    def record_pii_detection(self, entity_type: str, count: int = 1):
        """Record PII detection."""
        if self.enabled:
            PII_DETECTIONS.labels(entity_type=entity_type).inc(count)
    
    def record_security_violation(self, violation_type: str):
        """Record security violation."""
        if self.enabled:
            SECURITY_VIOLATIONS.labels(violation_type=violation_type).inc()
    
    def record_compliance_check(self, check_type: str, result: str):
        """Record compliance check result."""
        if self.enabled:
            COMPLIANCE_CHECKS.labels(
                check_type=check_type,
                result=result
            ).inc()
    
    def record_error(self, error_type: str, component: str):
        """Record an error."""
        if self.enabled:
            ERROR_RATE.labels(
                error_type=error_type,
                component=component
            ).inc()
    
    @contextmanager
    def track_active_request(self):
        """Context manager to track active requests."""
        if self.enabled:
            ACTIVE_REQUESTS.inc()
        try:
            yield
        finally:
            if self.enabled:
                ACTIVE_REQUESTS.dec()


def timed_operation(contract_type: str = "unknown", complexity: str = "unknown"):
    """Decorator to time operations and record metrics."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                
                # Try to extract actual contract type from result if available
                actual_type = contract_type
                actual_complexity = complexity
                
                if isinstance(result, dict):
                    actual_type = result.get('contract_type', contract_type)
                    actual_complexity = result.get('complexity', complexity)
                
                metrics.record_duration(actual_type, actual_complexity, duration)
                return result
                
            except Exception as e:
                metrics.record_error(type(e).__name__, func.__name__)
                raise
        
        return wrapper
    return decorator


# Global metrics instance
metrics = MetricsCollector()


# Import for context manager
from contextlib import contextmanager
