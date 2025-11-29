"""
Governance and compliance modules for Contract Analysis Agent.

This package provides:
- Audit Trail: Immutable, tamper-evident audit logging
- Policy Engine: Compliance policy evaluation
- Explainability: Structured explanations for AI decisions
- Guardrails: Responsible AI safety checks
"""

from .audit_trail import AuditTrail, AuditRecord, get_audit_trail
from .policy_engine import PolicyEngine, create_default_policies, get_policy_engine
from .explainability import ExplainabilityBuilder, create_sample_explanation
from .guardrails import Guardrails, create_default_guardrails, get_guardrails

__all__ = [
    # Audit Trail
    'AuditTrail',
    'AuditRecord',
    'get_audit_trail',
    
    # Policy Engine
    'PolicyEngine',
    'create_default_policies',
    'get_policy_engine',
    
    # Explainability
    'ExplainabilityBuilder',
    'create_sample_explanation',
    
    # Guardrails
    'Guardrails',
    'create_default_guardrails',
    'get_guardrails',
]
