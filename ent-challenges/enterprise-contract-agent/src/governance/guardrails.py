"""
Responsible AI Guardrails for Contract Analysis Agent
Enforces ethical, legal, and brand standards.
"""

import re
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class Guardrails:
    """
    Responsible AI guardrails to enforce safety and compliance.
    
    Categories:
    1. Content safety (harmful/biased language)
    2. Policy compliance (industry rules)
    3. Fairness checks (protected classes)
    4. Result confidence (fallback to human)
    """
    
    # Protected attributes (potential bias indicators)
    PROTECTED_TERMS = [
        "gender", "religion", "race", "ethnicity", "disability",
        "pregnant", "pregnancy", "age", "sexual orientation",
        "national origin", "veteran status"
    ]
    
    # Banned phrases (harmful content)
    BANNED_PHRASES = [
        "always reject", "refuse service", "terminate without cause",
        "discriminate", "exclude based on", "deny access to"
    ]
    
    def __init__(
        self,
        confidence_threshold: float = 0.6,
        enable_content_safety: bool = True,
        enable_bias_detection: bool = True,
        enable_confidence_check: bool = True
    ):
        """
        Initialize guardrails.
        
        Args:
            confidence_threshold: Minimum confidence for auto-approval
            enable_content_safety: Check for harmful content
            enable_bias_detection: Check for bias indicators
            enable_confidence_check: Require minimum confidence
        """
        self.confidence_threshold = confidence_threshold
        self.enable_content_safety = enable_content_safety
        self.enable_bias_detection = enable_bias_detection
        self.enable_confidence_check = enable_confidence_check
        
    def run_guardrails(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run all enabled guardrails against report.
        
        Args:
            report: Analysis report to check
            
        Returns:
            Dict with passed (bool), issues (list), and actions (list)
        """
        issues = []
        actions = []
        
        # Convert report to searchable text
        import json
        output_text = json.dumps(report).lower()
        
        # 1. Content Safety Check
        if self.enable_content_safety:
            content_issues = self._check_content_safety(output_text)
            issues.extend(content_issues)
            
            if content_issues:
                actions.append("Flag for content review")
        
        # 2. Bias Detection
        if self.enable_bias_detection:
            bias_issues = self._check_bias(output_text)
            issues.extend(bias_issues)
            
            if bias_issues:
                actions.append("Review for potential bias")
        
        # 3. Confidence Check
        if self.enable_confidence_check:
            confidence_issues = self._check_confidence(report)
            issues.extend(confidence_issues)
            
            if confidence_issues:
                actions.append("Escalate to human reviewer")
        
        # Determine overall pass/fail
        passed = len(issues) == 0
        severity_counts = {
            "critical": sum(1 for i in issues if i['severity'] == 'critical'),
            "high": sum(1 for i in issues if i['severity'] == 'high'),
            "medium": sum(1 for i in issues if i['severity'] == 'medium'),
            "low": sum(1 for i in issues if i['severity'] == 'low')
        }
        
        # Log results
        logger.info(
            "Guardrails evaluated",
            extra={
                "passed": passed,
                "issues_found": len(issues),
                "critical": severity_counts['critical'],
                "high": severity_counts['high']
            }
        )
        
        return {
            "passed": passed,
            "issues": issues,
            "actions": actions,
            "severity_counts": severity_counts,
            "requires_human_review": not passed or severity_counts['critical'] > 0
        }
    
    def _check_content_safety(self, text: str) -> List[Dict[str, Any]]:
        """Check for banned/harmful phrases."""
        issues = []
        
        for phrase in self.BANNED_PHRASES:
            if phrase in text:
                issues.append({
                    "type": "content_safety",
                    "message": f"Found banned phrase: '{phrase}'",
                    "severity": "high",
                    "phrase": phrase
                })
                logger.warning(f"Content safety violation: {phrase}")
        
        return issues
    
    def _check_bias(self, text: str) -> List[Dict[str, Any]]:
        """Check for protected attribute mentions."""
        issues = []
        
        for term in self.PROTECTED_TERMS:
            # Use word boundary to avoid partial matches
            pattern = r'\b' + re.escape(term) + r'\b'
            if re.search(pattern, text):
                issues.append({
                    "type": "bias_indicator",
                    "message": f"Mentions protected attribute: '{term}'",
                    "severity": "medium",
                    "term": term
                })
                logger.info(f"Bias indicator detected: {term}")
        
        return issues
    
    def _check_confidence(self, report: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check confidence thresholds."""
        issues = []
        
        confidence = report.get("confidence", 0.0)
        
        if confidence < self.confidence_threshold:
            issues.append({
                "type": "low_confidence",
                "message": f"Confidence {confidence:.1%} below threshold {self.confidence_threshold:.1%}",
                "severity": "high",
                "confidence": confidence,
                "threshold": self.confidence_threshold
            })
            logger.warning(f"Low confidence: {confidence:.1%}")
        
        # Check for missing required fields
        required_fields = ["contract_type", "risks", "summary"]
        missing = [f for f in required_fields if f not in report]
        
        if missing:
            issues.append({
                "type": "incomplete_analysis",
                "message": f"Missing required fields: {', '.join(missing)}",
                "severity": "critical",
                "missing_fields": missing
            })
            logger.error(f"Incomplete analysis: {missing}")
        
        return issues
    
    def add_custom_check(
        self,
        check_name: str,
        check_fn: callable,
        severity: str = "medium"
    ):
        """
        Add custom guardrail check.
        
        Args:
            check_name: Name of the check
            check_fn: Function that takes report and returns list of issues
            severity: Default severity for issues found
        """
        # Store for future use
        if not hasattr(self, '_custom_checks'):
            self._custom_checks = []
        
        self._custom_checks.append({
            "name": check_name,
            "function": check_fn,
            "severity": severity
        })
        
        logger.info(f"Custom guardrail added: {check_name}")


def create_default_guardrails() -> Guardrails:
    """
    Create guardrails with default configuration.
    
    Returns:
        Configured Guardrails instance
    """
    return Guardrails(
        confidence_threshold=0.6,
        enable_content_safety=True,
        enable_bias_detection=True,
        enable_confidence_check=True
    )


# Singleton instance
_guardrails = None


def get_guardrails() -> Guardrails:
    """Get or create default guardrails instance."""
    global _guardrails
    if _guardrails is None:
        _guardrails = create_default_guardrails()
    return _guardrails
