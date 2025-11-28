from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from ..config import Config
from ..prompts import RelevanceGraderPrompts


class GradeDocuments(BaseModel):
    """Binary score for relevance check on retrieved documents."""
    binary_score: str = Field(description="Documents are relevant to the question, 'yes' or 'no'")


class RelevanceGrader:
    """Document relevance grader."""
    
    def __init__(self, config: Config):
        self.config = config
        self._grader = None
    
    @property
    def grader(self):
        if self._grader is None:
            self._grader = self._create_relevance_grader()
        return self._grader
    
    def _create_relevance_grader(self):
        """Create the relevance grader chain."""
        llm_grader = AzureChatOpenAI(
            azure_endpoint=self.config.azure_endpoint,
            api_key=self.config.azure_api_key,
            azure_deployment=self.config.azure_deployment,
            api_version=self.config.azure_api_version,
            temperature=0
        )
        structured_llm_grader = llm_grader.with_structured_output(GradeDocuments)

        grade_prompt = ChatPromptTemplate.from_messages([
            ("system", RelevanceGraderPrompts.SYSTEM_PROMPT),
            ("human", "Retrieved document: \n\n {document} \n\n User question: {question}"),
        ])

        return grade_prompt | structured_llm_grader
    
    def grade(self, question: str, document: str) -> GradeDocuments:
        """Grade the relevance of a document to a question."""
        return self.grader.invoke({"question": question, "document": document})