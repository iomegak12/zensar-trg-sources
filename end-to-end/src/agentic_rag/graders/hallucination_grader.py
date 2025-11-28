from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from ..config import Config
from ..prompts import HallucinationGraderPrompts


class GradeHallucinations(BaseModel):
    """Binary score for hallucination present in generation answer."""
    binary_score: str = Field(description="Answer is grounded in the facts, 'yes' or 'no'")


class HallucinationGrader:
    """Hallucination grader."""
    
    def __init__(self, config: Config):
        self.config = config
        self._grader = None
    
    @property
    def grader(self):
        if self._grader is None:
            self._grader = self._create_hallucination_grader()
        return self._grader
    
    def _create_hallucination_grader(self):
        """Create the hallucination grader chain."""
        llm_hallucination = AzureChatOpenAI(
            azure_endpoint=self.config.azure_endpoint,
            api_key=self.config.azure_api_key,
            azure_deployment=self.config.azure_deployment,
            api_version=self.config.azure_api_version,
            temperature=0
        )
        structured_llm_hallucination = llm_hallucination.with_structured_output(GradeHallucinations)

        hallucination_prompt = ChatPromptTemplate.from_messages([
            ("system", HallucinationGraderPrompts.SYSTEM_PROMPT),
            ("human", "Set of facts: \n\n {documents} \n\n LLM generation: {generation}"),
        ])

        return hallucination_prompt | structured_llm_hallucination
    
    def grade(self, documents: str, generation: str) -> GradeHallucinations:
        """Grade whether a generation is grounded in the provided documents."""
        return self.grader.invoke({"documents": documents, "generation": generation})