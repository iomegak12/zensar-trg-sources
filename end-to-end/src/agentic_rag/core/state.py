from typing import TypedDict, List


class GraphState(TypedDict):
    """State of the agentic self-reflective RAG graph."""
    question: str
    generation: str
    documents: List[str]
    input_safe: str
    output_safe: str
    guardrail_message: str
    relevance_score: str
    hallucination_score: str
    answer_score: str
    rewrite_count: int
    tool_results: List[str]