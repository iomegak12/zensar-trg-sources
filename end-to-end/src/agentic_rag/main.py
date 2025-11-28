"""
Main AgenticRAG class - Simple interface for the Agentic Self-Reflective RAG system.
"""

from .config import Config


class AgenticRAG:
    """
    Agentic Self-Reflective RAG system.
    
    A production-ready RAG system with multi-tool routing, quality grading,
    and comprehensive guardrails using LangGraph and Azure OpenAI.
    """
    
    def __init__(self):
        """
        Initialize the AgenticRAG system.
        
        Loads configuration from environment variables and sets up the workflow.
        """
        print("Initializing Agentic RAG system...")
        
        # Load configuration first
        self.config = Config()
        print("✓ Configuration loaded")
        
        # Lazy import to avoid circular dependencies and import errors
        from .core import WorkflowBuilder
        
        # Build workflow
        workflow_builder = WorkflowBuilder(self.config)
        self.app = workflow_builder.build_workflow()
        print("✓ Workflow compiled successfully")
        print("🚀 Agentic RAG system ready!")
    
    def query(self, question: str, verbose: bool = False) -> dict:
        """
        Query the agentic self-reflective RAG system.
        
        Args:
            question: The user's question
            verbose: Whether to print processing details
        
        Returns:
            Dictionary containing the answer and metadata
        """
        # Execute the workflow
        result = self.app.invoke({"question": question})
        
        if verbose:
            self._print_processing_details(question, result)
        
        # Extract metadata for API response
        metadata = {
            "original_question": question,
            "rewritten_question": result.get('question'),
            "input_safe": result.get('input_safe'),
            "relevance_score": result.get('relevance_score'),
            "hallucination_score": result.get('hallucination_score'),
            "answer_score": result.get('answer_score'),
            "output_safe": result.get('output_safe'),
            "rewrite_count": result.get('rewrite_count', 0),
            "sources_used": result.get('documents', [])
        }
        
        return {
            "answer": result['generation'],
            "metadata": metadata
        }
    
    def _print_processing_details(self, original_question: str, result: dict):
        """Print detailed processing information."""
        print("\n" + "="*80)
        print("PROCESSING DETAILS")
        print("="*80)
        print(f"Original Question: {original_question}")
        if result.get('question') != original_question:
            print(f"Rewritten Question: {result['question']}")
        print(f"Input Safe: {result.get('input_safe', 'N/A')}")
        print(f"Relevance Score: {result.get('relevance_score', 'N/A')}")
        print(f"Hallucination Score: {result.get('hallucination_score', 'N/A')}")
        print(f"Answer Score: {result.get('answer_score', 'N/A')}")
        print(f"Output Safe: {result.get('output_safe', 'N/A')}")
        print(f"Rewrites: {result.get('rewrite_count', 0)}")
        print("="*80)