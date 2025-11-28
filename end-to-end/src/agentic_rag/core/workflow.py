from langgraph.graph import StateGraph, END
from .state import GraphState
from .nodes import NodeFunctions
from ..config import Config


class WorkflowBuilder:
    """Builder for the LangGraph workflow."""
    
    def __init__(self, config: Config):
        self.config = config
        self.node_functions = NodeFunctions(config)
    
    def build_workflow(self):
        """Build and compile the LangGraph workflow."""
        workflow = StateGraph(GraphState)

        # Add nodes
        workflow.add_node("check_input", self.node_functions.check_input_guardrail)
        workflow.add_node("route_tools", self.node_functions.route_to_tools)
        workflow.add_node("grade_docs", self.node_functions.grade_documents)
        workflow.add_node("generate", self.node_functions.generate)
        workflow.add_node("check_hallucination", self.node_functions.check_hallucination)
        workflow.add_node("grade_answer", self.node_functions.grade_answer)
        workflow.add_node("rewrite", self.node_functions.rewrite_question)
        workflow.add_node("check_output", self.node_functions.check_output_guardrail)

        # Set entry point
        workflow.set_entry_point("check_input")

        # Add edges
        workflow.add_conditional_edges(
            "check_input",
            self._decide_input_safety,
            {
                "safe": "route_tools",
                "unsafe": END
            }
        )

        workflow.add_edge("route_tools", "grade_docs")

        workflow.add_conditional_edges(
            "grade_docs",
            self._decide_relevance,
            {
                "relevant": "generate",
                "not_relevant": "rewrite"
            }
        )

        workflow.add_edge("rewrite", "route_tools")
        workflow.add_edge("generate", "check_hallucination")

        workflow.add_conditional_edges(
            "check_hallucination",
            self._decide_hallucination,
            {
                "grounded": "grade_answer",
                "not_grounded": "rewrite"
            }
        )

        workflow.add_conditional_edges(
            "grade_answer",
            self._decide_answer_quality,
            {
                "useful": "check_output",
                "not_useful": "rewrite",
                "max_rewrites": "check_output"
            }
        )

        workflow.add_conditional_edges(
            "check_output",
            self._decide_output_safety,
            {
                "safe": END,
                "unsafe": END
            }
        )

        # Compile the graph
        return workflow.compile()
    
    def _decide_input_safety(self, state: GraphState) -> str:
        """Determine if input is safe to process."""
        if state["input_safe"] == "yes":
            return "safe"
        else:
            return "unsafe"

    def _decide_relevance(self, state: GraphState) -> str:
        """Determine if documents are relevant."""
        if state["relevance_score"] == "yes":
            return "relevant"
        else:
            return "not_relevant"

    def _decide_hallucination(self, state: GraphState) -> str:
        """Determine if generation is grounded."""
        if state["hallucination_score"] == "yes":
            return "grounded"
        else:
            return "not_grounded"

    def _decide_answer_quality(self, state: GraphState) -> str:
        """Determine if answer addresses question."""
        rewrite_count = state.get("rewrite_count", 0)
        
        if state["answer_score"] == "yes":
            return "useful"
        elif rewrite_count < 2:  # Allow max 2 rewrites
            return "not_useful"
        else:
            return "max_rewrites"

    def _decide_output_safety(self, state: GraphState) -> str:
        """Determine if output is safe."""
        if state["output_safe"] == "yes":
            return "safe"
        else:
            return "unsafe"