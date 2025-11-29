"""
Policy Engine for Contract Analysis Agent
Evaluates compliance policies and regulatory requirements.
"""

from typing import List, Dict, Any, Callable
import logging

logger = logging.getLogger(__name__)


class PolicyEngine:
    """
    Lightweight policy engine for compliance evaluation.
    
    Policies are executable rules that return pass/fail with evidence.
    """
    
    def __init__(self, policies: List[Dict[str, Any]] = None):
        """
        Initialize policy engine.
        
        Args:
            policies: List of policy definitions with id, description, severity, and rule
        """
        self.policies = policies or []
        
    def add_policy(
        self,
        policy_id: str,
        description: str,
        severity: str,
        rule: Callable[[Dict[str, Any]], Dict[str, Any]]
    ):
        """
        Add a policy to the engine.
        
        Args:
            policy_id: Unique policy identifier (e.g., "GDPR-001")
            description: Human-readable description
            severity: "critical", "high", "medium", "low"
            rule: Function that takes context and returns {pass: bool, evidence: str}
        """
        self.policies.append({
            "id": policy_id,
            "description": description,
            "severity": severity,
            "rule": rule
        })
        
    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate all policies against context.
        
        Args:
            context: Dictionary with evaluation context
            
        Returns:
            Dict with passed (bool) and results (list of policy outcomes)
        """
        results = []
        passed = True
        
        for policy in self.policies:
            try:
                rule_fn = policy['rule']
                outcome = rule_fn(context)
                
                policy_passed = outcome.get('pass', False)
                passed = passed and policy_passed
                
                results.append({
                    "policy_id": policy['id'],
                    "description": policy['description'],
                    "pass": policy_passed,
                    "evidence": outcome.get('evidence', 'No evidence provided'),
                    "severity": policy['severity']
                })
                
                logger.info(
                    "Policy evaluated",
                    extra={
                        "policy_id": policy['id'],
                        "pass": policy_passed,
                        "severity": policy['severity']
                    }
                )
                
            except Exception as e:
                logger.error(f"Policy evaluation failed: {policy['id']}", exc_info=e)
                passed = False
                results.append({
                    "policy_id": policy['id'],
                    "description": policy['description'],
                    "pass": False,
                    "evidence": f"Evaluation error: {str(e)}",
                    "severity": policy['severity']
                })
        
        return {
            "passed": passed,
            "results": results,
            "total_policies": len(self.policies),
            "policies_passed": sum(1 for r in results if r['pass']),
            "policies_failed": sum(1 for r in results if not r['pass'])
        }
    
    def get_failed_policies(self, evaluation_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get list of failed policies from evaluation result."""
        return [r for r in evaluation_result['results'] if not r['pass']]
    
    def get_critical_failures(self, evaluation_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get list of critical severity failures."""
        return [
            r for r in evaluation_result['results']
            if not r['pass'] and r['severity'] == 'critical'
        ]


def create_default_policies() -> PolicyEngine:
    """
    Create policy engine with default compliance policies.
    
    Returns:
        PolicyEngine with pre-configured policies
    """
    policies = [
        {
            "id": "GDPR-001",
            "description": "PII must be redacted before export",
            "severity": "critical",
            "rule": lambda ctx: {
                "pass": not ctx.get("pii_detected", False) or ctx.get("pii_redacted", False),
                "evidence": f"PII detected: {ctx.get('pii_detected')} | Redacted: {ctx.get('pii_redacted')}"
            }
        },
        {
            "id": "SOC2-LOG",
            "description": "All analyses must have trace + audit record",
            "severity": "high",
            "rule": lambda ctx: {
                "pass": all([
                    ctx.get("trace_id"),
                    ctx.get("audit_hash"),
                    ctx.get("logs_written")
                ]),
                "evidence": f"Trace: {ctx.get('trace_id')} | Audit: {ctx.get('audit_hash')} | Logs: {ctx.get('logs_written')}"
            }
        },
        {
            "id": "RISK-007",
            "description": "High-risk contracts require manual approval",
            "severity": "medium",
            "rule": lambda ctx: {
                "pass": ctx.get("risk_level") != "high" or ctx.get("human_approved", False),
                "evidence": f"Risk: {ctx.get('risk_level')} | Human approved: {ctx.get('human_approved')}"
            }
        },
        {
            "id": "DATA-RET",
            "description": "Analysis retention policy must be set",
            "severity": "low",
            "rule": lambda ctx: {
                "pass": ctx.get("retention_days") is not None,
                "evidence": f"Retention: {ctx.get('retention_days')} days"
            }
        },
        {
            "id": "AUTH-001",
            "description": "User must be authenticated",
            "severity": "critical",
            "rule": lambda ctx: {
                "pass": bool(ctx.get("user_id")),
                "evidence": f"User ID: {ctx.get('user_id')}"
            }
        }
    ]
    
    return PolicyEngine(policies)


# Singleton instance
_policy_engine = None


def get_policy_engine() -> PolicyEngine:
    """Get or create default policy engine instance."""
    global _policy_engine
    if _policy_engine is None:
        _policy_engine = create_default_policies()
    return _policy_engine
