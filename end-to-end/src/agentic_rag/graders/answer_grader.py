from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from ..config import Config
from ..prompts import AnswerGraderPrompts


class GradeAnswer(BaseModel):
    """Binary score to assess answer addresses question."""
    binary_score: str = Field(description="Answer addresses the question, 'yes' or 'no'")


class AnswerGrader:
    """Answer quality grader."""
    
    def __init__(self, config: Config):
        self.config = config
        self._grader = None
    
    @property
    def grader(self):
        if self._grader is None:
            self._grader = self._create_answer_grader()
        return self._grader
    
    def _create_answer_grader(self):
        """Create the answer grader chain."""
        llm_answer = AzureChatOpenAI(
            azure_endpoint=self.config.azure_endpoint,
            api_key=self.config.azure_api_key,
            azure_deployment=self.config.azure_deployment,
            api_version=self.config.azure_api_version,
            temperature=0
        )
        structured_llm_answer = llm_answer.with_structured_output(GradeAnswer)

        answer_prompt = ChatPromptTemplate.from_messages([
            ("system", AnswerGraderPrompts.SYSTEM_PROMPT),
            ("human", "User question: \n\n {question} \n\n LLM generation: {generation}"),
        ])

        return answer_prompt | structured_llm_answer
    
    def grade(self, question: str, generation: str) -> GradeAnswer:
        """Grade whether an answer addresses the question."""
        return self.grader.invoke({"question": question, "generation": generation})