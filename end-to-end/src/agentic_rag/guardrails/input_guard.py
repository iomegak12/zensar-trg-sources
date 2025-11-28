from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from ..config import Config
from ..prompts import InputGuardrailPrompts


class GuardrailInput(BaseModel):
    """Safety and policy check for input questions."""
    
    is_safe: str = Field(description="Question is safe and appropriate, 'yes' or 'no'")
    concern_type: str = Field(description="Type of concern if unsafe: 'none', 'harmful', 'pii', 'injection', 'off_topic', or 'other'")
    explanation: str = Field(description="Brief explanation of the decision")


class InputGuardrail:
    """Input safety guardrail checker."""
    
    def __init__(self, config: Config):
        self.config = config
        self._guardrail = None
    
    @property
    def guardrail(self):
        if self._guardrail is None:
            self._guardrail = self._create_input_guardrail()
        return self._guardrail
    
    def _create_input_guardrail(self):
        """Create the input guardrail chain."""
        llm_input_guard = AzureChatOpenAI(
            azure_endpoint=self.config.azure_endpoint,
            api_key=self.config.azure_api_key,
            azure_deployment=self.config.azure_deployment,
            api_version=self.config.azure_api_version,
            temperature=0
        )
        structured_llm_input_guard = llm_input_guard.with_structured_output(GuardrailInput)

        input_guard_prompt = ChatPromptTemplate.from_messages([
            ("system", InputGuardrailPrompts.SYSTEM_PROMPT),
            ("human", "User question: {question}"),
        ])

        return input_guard_prompt | structured_llm_input_guard
    
    def check(self, question: str) -> GuardrailInput:
        """Check if a question passes safety guardrails."""
        return self.guardrail.invoke({"question": question})