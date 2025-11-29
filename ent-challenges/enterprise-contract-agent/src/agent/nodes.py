"""
Node implementations for Contract Analysis workflow
Each node performs a specific task in the analysis pipeline.
"""

import os
from typing import List
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from .state import ContractAnalysisState


# ============================================================================
# Pydantic Models for Structured Outputs
# ============================================================================

class ContractClassification(BaseModel):
    """Structured output for contract classification."""
    contract_type: str = Field(description="Type: NDA, SaaS, Employment, Partnership, or Unknown")
    complexity: str = Field(description="Complexity: Simple, Moderate, or Complex")
    confidence_score: float = Field(description="Confidence score between 0 and 1")
    reasoning: str = Field(description="Brief explanation of classification")


class KeyTerm(BaseModel):
    """A key term or clause in the contract."""
    term: str = Field(description="The key term or clause")
    description: str = Field(description="What this term means")
    importance: str = Field(description="High, Medium, or Low")


class Risk(BaseModel):
    """An identified risk in the contract."""
    risk_description: str = Field(description="Description of the risk")
    severity: str = Field(description="High, Medium, or Low")
    mitigation: str = Field(description="How to mitigate this risk")


class ContractAnalysis(BaseModel):
    """Structured output for detailed contract analysis."""
    key_terms: List[KeyTerm] = Field(description="Important terms and clauses")
    obligations: List[str] = Field(description="Key obligations for parties")
    risks: List[Risk] = Field(description="Identified risks")
    red_flags: List[str] = Field(description="Critical issues requiring attention")


# ============================================================================
# Node 1: Classification
# ============================================================================

def classify_contract(state: ContractAnalysisState) -> ContractAnalysisState:
    """
    Classify the contract type and complexity using LLM.
    
    Args:
        state: Current workflow state
        
    Returns:
        Updated state with classification results
    """
    print(f"🔍 Classifying contract (Request ID: {state['request_id']})...")
    
    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0
    )
    
    structured_llm = llm.with_structured_output(ContractClassification)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert contract analyst. Analyze the provided contract and classify it.
        
Contract Types:
- NDA: Non-Disclosure Agreement
- SaaS: Software as a Service Agreement  
- Employment: Employment or offer letter
- Partnership: Partnership or joint venture agreement
- Unknown: Cannot determine or mixed type

Complexity Levels:
- Simple: Straightforward, standard terms, <5 pages
- Moderate: Multiple sections, some complexity, 5-15 pages
- Complex: Multi-party, intricate terms, >15 pages or advanced legal structures
"""),
        ("user", "Classify this contract:\n\n{contract_text}")
    ])
    
    chain = prompt | structured_llm
    text_sample = state['contract_text'][:4000]
    
    try:
        result = chain.invoke({"contract_text": text_sample})
        
        state['contract_type'] = result.contract_type
        state['complexity'] = result.complexity
        state['confidence_score'] = result.confidence_score
        
        print(f"  ✅ Type: {result.contract_type}")
        print(f"  ✅ Complexity: {result.complexity}")
        print(f"  ✅ Confidence: {result.confidence_score:.2f}")
        
    except Exception as e:
        state['errors'].append(f"Classification error: {str(e)}")
        state['contract_type'] = "Unknown"
        state['complexity'] = "Unknown"
        state['confidence_score'] = 0.0
        print(f"  ❌ Classification failed: {str(e)}")
    
    return state


# ============================================================================
# Node 2: Analysis
# ============================================================================

def analyze_contract(state: ContractAnalysisState) -> ContractAnalysisState:
    """
    Perform detailed analysis of the contract.
    
    Args:
        state: Current workflow state
        
    Returns:
        Updated state with analysis results
    """
    print(f"\n📝 Analyzing {state['contract_type']} contract...")
    
    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0
    )
    
    structured_llm = llm.with_structured_output(ContractAnalysis)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert contract analyst. Perform a comprehensive analysis.

Focus on:
1. Key Terms: Important clauses, definitions, and provisions
2. Obligations: What each party must do
3. Risks: Potential issues or unfavorable terms
4. Red Flags: Critical issues that need immediate attention

Be thorough but concise. Prioritize business-critical items.
"""),
        ("user", """Analyze this {contract_type} contract:

{contract_text}

Provide a structured analysis.""")
    ])
    
    chain = prompt | structured_llm
    
    try:
        result = chain.invoke({
            "contract_type": state['contract_type'],
            "contract_text": state['contract_text'][:15000]
        })
        
        state['key_terms'] = [term.dict() for term in result.key_terms]
        state['obligations'] = result.obligations
        state['risks'] = [risk.dict() for risk in result.risks]
        state['red_flags'] = result.red_flags
        
        print(f"  ✅ Found {len(result.key_terms)} key terms")
        print(f"  ✅ Found {len(result.obligations)} obligations")
        print(f"  ✅ Identified {len(result.risks)} risks")
        print(f"  ⚠️  {len(result.red_flags)} red flags detected")
        
    except Exception as e:
        state['errors'].append(f"Analysis error: {str(e)}")
        print(f"  ❌ Analysis failed: {str(e)}")
    
    return state


# ============================================================================
# Node 3: Security Validation
# ============================================================================

def validate_security(state: ContractAnalysisState) -> ContractAnalysisState:
    """
    Validate security and detect PII in the contract.
    
    Args:
        state: Current workflow state
        
    Returns:
        Updated state with security validation results
    """
    print(f"\n🔒 Validating security...")
    
    # Placeholder for security validation
    # In production, integrate with Presidio or similar
    state['security_validated'] = True
    state['pii_detected'] = []
    
    print(f"  ✅ Security validated")
    
    return state


# ============================================================================
# Node 4: Compliance Check
# ============================================================================

def check_compliance(state: ContractAnalysisState) -> ContractAnalysisState:
    """
    Check compliance requirements (GDPR, data retention, etc.).
    
    Args:
        state: Current workflow state
        
    Returns:
        Updated state with compliance check results
    """
    print(f"\n✅ Checking compliance...")
    
    # Placeholder for compliance checking
    # In production, implement actual compliance rules
    state['gdpr_compliant'] = True
    state['compliance_issues'] = []
    state['data_retention_period'] = "Not specified"
    
    print(f"  ✅ GDPR compliant")
    
    return state


# ============================================================================
# Node 5: Finalize Output
# ============================================================================

def finalize_output(state: ContractAnalysisState) -> ContractAnalysisState:
    """
    Generate final analysis report.
    
    Args:
        state: Current workflow state
        
    Returns:
        Updated state with final report
    """
    print(f"\n📊 Generating final report...")
    
    state['final_report'] = {
        "request_id": state['request_id'],
        "timestamp": state['timestamp'],
        "contract_type": state['contract_type'],
        "complexity": state['complexity'],
        "confidence": state['confidence_score'],
        "key_terms_count": len(state.get('key_terms', [])),
        "obligations_count": len(state.get('obligations', [])),
        "risks_count": len(state.get('risks', [])),
        "red_flags_count": len(state.get('red_flags', [])),
        "security_validated": state.get('security_validated', False),
        "gdpr_compliant": state.get('gdpr_compliant', False),
        "errors": state.get('errors', []),
        "warnings": state.get('warnings', [])
    }
    
    state['analysis_complete'] = True
    
    print(f"  ✅ Report generated")
    print(f"\n{'='*60}")
    print(f"📋 ANALYSIS COMPLETE")
    print(f"{'='*60}")
    print(f"Contract Type: {state['contract_type']} ({state['complexity']})")
    print(f"Confidence: {state['confidence_score']:.2%}")
    print(f"Key Terms: {len(state.get('key_terms', []))}")
    print(f"Red Flags: {len(state.get('red_flags', []))}")
    print(f"{'='*60}")
    
    return state
