"""
State definition for Contract Analysis Agent
Defines the state structure used throughout the LangGraph workflow.
"""

from typing import TypedDict, List, Optional, Dict, Any
from datetime import datetime
import uuid


class ContractAnalysisState(TypedDict):
    """State object for contract analysis workflow."""
    
    # Input fields
    contract_text: str
    file_path: Optional[str]
    user_id: str
    request_id: str
    timestamp: str
    
    # Classification results
    contract_type: Optional[str]
    complexity: Optional[str]
    confidence_score: Optional[float]
    
    # Analysis results
    key_terms: Optional[List[Dict[str, Any]]]
    obligations: Optional[List[str]]
    risks: Optional[List[Dict[str, Any]]]
    red_flags: Optional[List[str]]
    
    # Security & PII
    pii_detected: Optional[List[Dict[str, Any]]]
    security_validated: Optional[bool]
    
    # Compliance
    gdpr_compliant: Optional[bool]
    compliance_issues: Optional[List[str]]
    data_retention_period: Optional[str]
    
    # Observability
    trace_id: Optional[str]
    errors: Optional[List[str]]
    warnings: Optional[List[str]]
    
    # Governance
    explainability: Optional[Dict[str, Any]]
    bias_check: Optional[Dict[str, Any]]
    
    # Output
    analysis_complete: bool
    final_report: Optional[Dict[str, Any]]


def create_initial_state(
    contract_text: str,
    file_path: Optional[str] = None,
    user_id: str = "system"
) -> ContractAnalysisState:
    """
    Create initial state for contract analysis.
    
    Args:
        contract_text: The contract text to analyze
        file_path: Optional path to the source file
        user_id: User ID initiating the analysis
        
    Returns:
        Initial ContractAnalysisState
    """
    return ContractAnalysisState(
        contract_text=contract_text,
        file_path=file_path,
        user_id=user_id,
        request_id=str(uuid.uuid4()),
        timestamp=datetime.utcnow().isoformat(),
        contract_type=None,
        complexity=None,
        confidence_score=None,
        key_terms=None,
        obligations=None,
        risks=None,
        red_flags=None,
        pii_detected=None,
        security_validated=None,
        gdpr_compliant=None,
        compliance_issues=None,
        data_retention_period=None,
        trace_id=None,
        errors=[],
        warnings=[],
        explainability=None,
        bias_check=None,
        analysis_complete=False,
        final_report=None
    )
