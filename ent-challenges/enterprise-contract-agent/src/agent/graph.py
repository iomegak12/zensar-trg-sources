"""
LangGraph workflow definition for Contract Analysis
Connects all nodes into a complete analysis pipeline.
"""

import fitz  # PyMuPDF
from pathlib import Path
from langgraph.graph import StateGraph, END

from .state import ContractAnalysisState, create_initial_state
from .nodes import (
    classify_contract,
    analyze_contract,
    validate_security,
    check_compliance,
    finalize_output
)


def create_contract_analysis_graph():
    """
    Create the LangGraph workflow for contract analysis.
    
    Returns:
        Compiled LangGraph workflow
    """
    # Initialize graph with state type
    workflow = StateGraph(ContractAnalysisState)
    
    # Add nodes
    workflow.add_node("classify", classify_contract)
    workflow.add_node("analyze", analyze_contract)
    workflow.add_node("security", validate_security)
    workflow.add_node("compliance", check_compliance)
    workflow.add_node("finalize", finalize_output)
    
    # Define edges (workflow sequence)
    workflow.set_entry_point("classify")
    workflow.add_edge("classify", "analyze")
    workflow.add_edge("analyze", "security")
    workflow.add_edge("security", "compliance")
    workflow.add_edge("compliance", "finalize")
    workflow.add_edge("finalize", END)
    
    # Compile the graph
    app = workflow.compile()
    
    return app


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text content from a PDF file using PyMuPDF.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Extracted text as a string
    """
    try:
        doc = fitz.open(pdf_path)
        text_parts = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text_parts.append(page.get_text())
        
        doc.close()
        full_text = "\n".join(text_parts)
        
        return full_text.strip()
    
    except Exception as e:
        raise ValueError(f"Error extracting text from PDF: {str(e)}")


def analyze_contract_file(file_path: str, user_id: str = "system") -> dict:
    """
    Analyze a contract file end-to-end.
    
    Args:
        file_path: Path to the contract PDF file
        user_id: User ID initiating the analysis
        
    Returns:
        Final analysis report
    """
    # Extract text from PDF
    print(f"📄 Extracting text from {Path(file_path).name}...")
    contract_text = extract_text_from_pdf(file_path)
    print(f"  ✅ Extracted {len(contract_text)} characters\n")
    
    # Create initial state
    initial_state = create_initial_state(
        contract_text=contract_text,
        file_path=file_path,
        user_id=user_id
    )
    
    # Create and run the graph
    graph = create_contract_analysis_graph()
    final_state = graph.invoke(initial_state)
    
    return final_state['final_report']
