"""
OpenTelemetry Tracer Configuration for Contract Analysis Agent
Provides distributed tracing capabilities for monitoring agent workflow.
"""

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.trace import Status, StatusCode
from contextlib import contextmanager
import os
import logging

logger = logging.getLogger(__name__)


class ContractAgentTracer:
    """Manages OpenTelemetry tracing for the contract analysis agent."""
    
    def __init__(self, service_name: str = "contract-analysis-agent"):
        """
        Initialize the tracer.
        
        Args:
            service_name: Name of the service for tracing
        """
        self.service_name = service_name
        self.enabled = os.getenv("ENABLE_OBSERVABILITY", "true").lower() == "true"
        
        if self.enabled:
            self._setup_tracer()
        else:
            logger.info("Observability disabled")
    
    def _setup_tracer(self):
        """Configure OpenTelemetry tracer and exporter."""
        try:
            # Create resource with service name
            resource = Resource.create({
                "service.name": self.service_name,
                "service.version": "1.0.0"
            })
            
            # Initialize tracer provider
            provider = TracerProvider(resource=resource)
            
            # Configure OTLP exporter
            otlp_endpoint = os.getenv(
                "OTEL_EXPORTER_OTLP_ENDPOINT",
                "http://localhost:4318"
            )
            
            otlp_exporter = OTLPSpanExporter(
                endpoint=f"{otlp_endpoint}/v1/traces"
            )
            
            # Add span processor
            provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
            
            # Set as global tracer provider
            trace.set_tracer_provider(provider)
            
            self.tracer = trace.get_tracer(__name__)
            logger.info(f"✅ OpenTelemetry tracer initialized (endpoint: {otlp_endpoint})")
            
        except Exception as e:
            logger.error(f"Failed to initialize tracer: {e}")
            self.enabled = False
            self.tracer = trace.get_tracer(__name__)  # Use no-op tracer
    
    @contextmanager
    def trace_span(self, span_name: str, attributes: dict = None):
        """
        Context manager for creating traced spans.
        
        Args:
            span_name: Name of the span
            attributes: Optional attributes to attach to the span
            
        Yields:
            Span object
        """
        if not self.enabled:
            yield None
            return
        
        with self.tracer.start_as_current_span(span_name) as span:
            if attributes:
                for key, value in attributes.items():
                    span.set_attribute(key, value)
            
            try:
                yield span
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.record_exception(e)
                raise
    
    def add_span_event(self, event_name: str, attributes: dict = None):
        """
        Add an event to the current span.
        
        Args:
            event_name: Name of the event
            attributes: Optional event attributes
        """
        if not self.enabled:
            return
        
        current_span = trace.get_current_span()
        if current_span:
            current_span.add_event(event_name, attributes or {})


# Global tracer instance
_tracer_instance = None


def get_tracer() -> ContractAgentTracer:
    """Get or create the global tracer instance."""
    global _tracer_instance
    if _tracer_instance is None:
        _tracer_instance = ContractAgentTracer()
    return _tracer_instance
