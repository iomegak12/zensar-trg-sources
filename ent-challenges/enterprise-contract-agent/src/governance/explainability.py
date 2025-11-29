"""
Explainability Engine for Contract Analysis Agent
Provides structured explanations for AI decisions.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class ExplainabilityBuilder:
    """
    Builds structured explanations for AI decisions.
    
    Every AI decision must answer:
    1. Why was this answer produced?
    2. What evidence supports it?
    """
    
    @staticmethod
    def build_explanation(
        contract_type: str,
        classification_reasoning: str,
        risks: List[Dict[str, Any]],
        confidence: float,
        key_clauses: List[str],
        additional_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Build structured explanation for contract analysis.
        
        Args:
            contract_type: Classified contract type
            classification_reasoning: LLM's reasoning for classification
            risks: List of identified risks
            confidence: Confidence score (0-1)
            key_clauses: Important contract clauses
            additional_context: Optional additional context
            
        Returns:
            Structured explanation dictionary
        """
        explanation = {
            "summary": f"Classified as {contract_type} with confidence {confidence:.0%}.",
            "reasoning_steps": [
                "Analyzed clause structure and keywords.",
                f"Applied contract taxonomy to classify as {contract_type}.",
                "Evaluated obligations and risk statements.",
                "Compared against compliance policy requirements."
            ],
            "llm_reasoning": classification_reasoning,
            "confidence_breakdown": {
                "contract_type": confidence,
                "risk_assessment": confidence * 0.9,
                "clause_extraction": confidence * 0.95
            },
            "evidence": {
                "key_risks": risks,
                "clauses": key_clauses,
                "risk_count": len(risks),
                "high_severity_risks": sum(1 for r in risks if r.get('severity') == 'HIGH')
            },
            "human_review_required": any(
                r.get('severity') == 'HIGH' for r in risks
            ) or confidence < 0.7,
            "created_at": datetime.utcnow().isoformat()
        }
        
        if additional_context:
            explanation["additional_context"] = additional_context
        
        logger.info(
            "Explanation generated",
            extra={
                "contract_type": contract_type,
                "confidence": confidence,
                "risks_found": len(risks),
                "human_review": explanation["human_review_required"]
            }
        )
        
        return explanation
    
    @staticmethod
    def format_for_human(explanation: Dict[str, Any]) -> str:
        """
        Format explanation as human-readable text.
        
        Args:
            explanation: Structured explanation
            
        Returns:
            Formatted string
        """
        lines = [
            "=" * 80,
            "CONTRACT ANALYSIS EXPLANATION",
            "=" * 80,
            "",
            f"Summary: {explanation['summary']}",
            "",
            "Reasoning Process:",
        ]
        
        for i, step in enumerate(explanation['reasoning_steps'], 1):
            lines.append(f"  {i}. {step}")
        
        lines.extend([
            "",
            "LLM Reasoning:",
            f"  {explanation['llm_reasoning']}",
            "",
            "Confidence Scores:"
        ])
        
        for metric, score in explanation['confidence_breakdown'].items():
            lines.append(f"  • {metric}: {score:.1%}")
        
        lines.extend([
            "",
            "Evidence:",
            f"  • Total Risks: {explanation['evidence']['risk_count']}",
            f"  • High Severity: {explanation['evidence']['high_severity_risks']}",
            f"  • Key Clauses: {len(explanation['evidence']['clauses'])}"
        ])
        
        if explanation['evidence']['key_risks']:
            lines.append("")
            lines.append("  Top Risks:")
            for risk in explanation['evidence']['key_risks'][:3]:
                severity = risk.get('severity', 'UNKNOWN')
                description = risk.get('risk', 'No description')
                lines.append(f"    • [{severity}] {description}")
        
        lines.extend([
            "",
            f"Human Review Required: {'YES' if explanation['human_review_required'] else 'NO'}",
            "",
            "=" * 80
        ])
        
        return "\n".join(lines)
    
    @staticmethod
    def add_citation(
        explanation: Dict[str, Any],
        source: str,
        quote: str,
        relevance: str
    ) -> Dict[str, Any]:
        """
        Add source citation to explanation.
        
        Args:
            explanation: Existing explanation
            source: Source identifier (e.g., "Section 3.2")
            quote: Quoted text
            relevance: Why this citation matters
            
        Returns:
            Updated explanation
        """
        if 'citations' not in explanation:
            explanation['citations'] = []
        
        explanation['citations'].append({
            "source": source,
            "quote": quote,
            "relevance": relevance,
            "added_at": datetime.utcnow().isoformat()
        })
        
        return explanation
    
    @staticmethod
    def add_assumption(
        explanation: Dict[str, Any],
        assumption: str,
        rationale: str
    ) -> Dict[str, Any]:
        """
        Document assumptions made during analysis.
        
        Args:
            explanation: Existing explanation
            assumption: The assumption made
            rationale: Why this assumption was necessary
            
        Returns:
            Updated explanation
        """
        if 'assumptions' not in explanation:
            explanation['assumptions'] = []
        
        explanation['assumptions'].append({
            "assumption": assumption,
            "rationale": rationale,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        return explanation
    
    @staticmethod
    def add_limitation(
        explanation: Dict[str, Any],
        limitation: str,
        impact: str
    ) -> Dict[str, Any]:
        """
        Document limitations of the analysis.
        
        Args:
            explanation: Existing explanation
            limitation: The limitation
            impact: How this affects the result
            
        Returns:
            Updated explanation
        """
        if 'limitations' not in explanation:
            explanation['limitations'] = []
        
        explanation['limitations'].append({
            "limitation": limitation,
            "impact": impact,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        return explanation


def create_sample_explanation() -> Dict[str, Any]:
    """
    Create a sample explanation for demonstration.
    
    Returns:
        Sample structured explanation
    """
    return ExplainabilityBuilder.build_explanation(
        contract_type="SaaS Agreement",
        classification_reasoning="Contains subscription language, uptime SLAs, and multi-tenant references typical of Software-as-a-Service agreements.",
        risks=[
            {"risk": "No explicit data portability clause", "severity": "HIGH"},
            {"risk": "Auto-renewal without notification", "severity": "MEDIUM"},
            {"risk": "Vendor lock-in through proprietary APIs", "severity": "MEDIUM"}
        ],
        confidence=0.87,
        key_clauses=[
            "Section 3.2: Service Level Agreement (99.9% uptime)",
            "Section 5.1: Term & Renewal (automatic annual renewal)",
            "Section 7: Data Processing and Storage"
        ]
    )
