"""
Root package init for Contract Analysis Agent
"""

__version__ = "1.0.0"
__author__ = "AI for Leaders Training"

from .agent import create_contract_analysis_graph, analyze_contract_file
from .observability import get_tracer, metrics, logger
from .security import get_pii_detector, get_validator, get_rate_limiter

__all__ = [
    'create_contract_analysis_graph',
    'analyze_contract_file',
    'get_tracer',
    'metrics',
    'logger',
    'get_pii_detector',
    'get_validator',
    'get_rate_limiter'
]
