from typing import List
from langchain_openai import AzureChatOpenAI
from .state import GraphState
from ..config import Config
from ..tools import GoogleSearchTool, WikipediaSearchTool, ArxivSearchTool, VectorStoreRetrieverTool
from ..guardrails import InputGuardrail, OutputGuardrail
from ..graders import RelevanceGrader, HallucinationGrader, AnswerGrader, QuestionRewriter
from ..core.generator import AnswerGenerator


class NodeFunctions:
    """All node functions for the LangGraph workflow."""
    
    def __init__(self, config: Config):
        self.config = config
        
        # Initialize tools
        self.google_tool = GoogleSearchTool(config)
        self.wiki_tool = WikipediaSearchTool(config)
        self.arxiv_tool = ArxivSearchTool(config)
        self.retriever_tool = VectorStoreRetrieverTool(config)
        
        # Combine tools
        self.tools = [
            self.arxiv_tool.tool,
            self.google_tool.tool,
            self.wiki_tool.tool,
            self.retriever_tool.tool
        ]
        
        # Initialize guardrails
        self.input_guard = InputGuardrail(config)
        self.output_guard = OutputGuardrail(config)
        
        # Initialize graders
        self.relevance_grader = RelevanceGrader(config)
        self.hallucination_grader = HallucinationGrader(config)
        self.answer_grader = AnswerGrader(config)
        self.question_rewriter = QuestionRewriter(config)
        
        # Initialize generator
        self.answer_generator = AnswerGenerator(config)
        
        # Initialize LLM for tool routing
        self.llm = AzureChatOpenAI(
            azure_endpoint=config.azure_endpoint,
            api_key=config.azure_api_key,
            azure_deployment=config.azure_deployment,
            api_version=config.azure_api_version,
            temperature=0,
            max_tokens=2000
        )
    
    def check_input_guardrail(self, state: GraphState) -> GraphState:
        """Check if input question passes safety guardrails."""
        print("---CHECK INPUT GUARDRAILS---")
        question = state["question"]
        
        guard_result = self.input_guard.check(question)
        
        if guard_result.is_safe == "yes":
            print("---INPUT GUARDRAIL PASSED---")
            return {"question": question, "input_safe": "yes", "rewrite_count": 0}
        else:
            print(f"---INPUT GUARDRAIL FAILED: {guard_result.concern_type}---")
            message = f"I cannot process this request. Reason: {guard_result.explanation}"
            return {
                "question": question,
                "input_safe": "no",
                "guardrail_message": message,
                "generation": message
            }

    def route_to_tools(self, state: GraphState) -> GraphState:
        """Use LLM with tools to retrieve information from appropriate sources."""
        print("---ROUTE TO TOOLS---")
        question = state["question"]
        
        # Bind tools to LLM
        llm_with_tools = self.llm.bind_tools(self.tools)
        
        # Invoke with question
        response = llm_with_tools.invoke(question)
        
        # Execute tools if called
        tool_results = []
        if hasattr(response, 'tool_calls') and response.tool_calls:
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                
                print(f"---EXECUTING TOOL: {tool_name}---")
                
                # Find and execute the tool
                for tool in self.tools:
                    if tool.name == tool_name:
                        result = tool.invoke(tool_args)
                        tool_results.append(str(result))
                        break
        else:
            # If no tools called, use response content
            tool_results.append(response.content)
        
        return {
            "question": question,
            "tool_results": tool_results,
            "documents": tool_results
        }

    def grade_documents(self, state: GraphState) -> GraphState:
        """Grade the relevance of retrieved documents."""
        print("---GRADE DOCUMENTS---")
        question = state["question"]
        documents = state["documents"]
        
        filtered_docs = []
        for doc in documents:
            score = self.relevance_grader.grade(question, doc)
            if score.binary_score == "yes":
                print("---GRADE: DOCUMENT RELEVANT---")
                filtered_docs.append(doc)
            else:
                print("---GRADE: DOCUMENT NOT RELEVANT---")
        
        relevance = "yes" if filtered_docs else "no"
        
        return {
            "question": question,
            "documents": filtered_docs,
            "relevance_score": relevance
        }

    def generate(self, state: GraphState) -> GraphState:
        """Generate answer based on retrieved documents."""
        print("---GENERATE---")
        question = state["question"]
        documents = state["documents"]
        
        context = "\n\n".join(documents)
        generation = self.answer_generator.generate(context, question)
        
        return {
            "question": question,
            "documents": documents,
            "generation": generation
        }

    def check_hallucination(self, state: GraphState) -> GraphState:
        """Check if generation is grounded in documents."""
        print("---CHECK HALLUCINATION---")
        question = state["question"]
        documents = state["documents"]
        generation = state["generation"]
        
        docs_text = "\n\n".join(documents)
        score = self.hallucination_grader.grade(docs_text, generation)
        
        if score.binary_score == "yes":
            print("---DECISION: GENERATION IS GROUNDED IN DOCUMENTS---")
        else:
            print("---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS---")
        
        return {
            "question": question,
            "documents": documents,
            "generation": generation,
            "hallucination_score": score.binary_score
        }

    def grade_answer(self, state: GraphState) -> GraphState:
        """Check if answer addresses the question."""
        print("---GRADE ANSWER---")
        question = state["question"]
        generation = state["generation"]
        
        score = self.answer_grader.grade(question, generation)
        
        if score.binary_score == "yes":
            print("---DECISION: ANSWER ADDRESSES QUESTION---")
        else:
            print("---DECISION: ANSWER DOES NOT ADDRESS QUESTION---")
        
        return {
            "question": question,
            "generation": generation,
            "answer_score": score.binary_score
        }

    def rewrite_question(self, state: GraphState) -> GraphState:
        """Rewrite the question to improve retrieval."""
        print("---REWRITE QUESTION---")
        question = state["question"]
        rewrite_count = state.get("rewrite_count", 0)
        
        better_question = self.question_rewriter.rewrite(question)
        print(f"---REWRITTEN: {better_question}---")
        
        return {
            "question": better_question,
            "rewrite_count": rewrite_count + 1
        }

    def check_output_guardrail(self, state: GraphState) -> GraphState:
        """Check if output passes safety guardrails."""
        print("---CHECK OUTPUT GUARDRAILS---")
        question = state["question"]
        generation = state["generation"]
        
        guard_result = self.output_guard.check(question, generation)
        
        if guard_result.is_safe == "yes":
            print("---OUTPUT GUARDRAIL PASSED---")
            return {
                "question": question,
                "generation": generation,
                "output_safe": "yes"
            }
        else:
            print(f"---OUTPUT GUARDRAIL FAILED: {guard_result.concern_type}---")
            message = f"I cannot provide this response. Reason: {guard_result.explanation}"
            return {
                "question": question,
                "generation": message,
                "output_safe": "no",
                "guardrail_message": message
            }