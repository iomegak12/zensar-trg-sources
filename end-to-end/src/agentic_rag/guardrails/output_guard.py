from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from ..config import Config
from ..prompts import OutputGuardrailPrompts


class GuardrailOutput(BaseModel):
    """Safety and policy check for generated responses."""
    
    is_safe: str = Field(description="Response is safe and appropriate, 'yes' or 'no'")
    concern_type: str = Field(description="Type of concern if unsafe: 'none', 'harmful', 'pii', 'bias', 'misinformation', or 'other'")
    explanation: str = Field(description="Brief explanation of the decision")


class OutputGuardrail:
    """Output safety guardrail checker."""
    
    def __init__(self, config: Config):
        self.config = config
        self._guardrail = None
    
    @property
    def guardrail(self):
        if self._guardrail is None:
            self._guardrail = self._create_output_guardrail()
        return self._guardrail
    
    def _create_output_guardrail(self):
        """Create the output guardrail chain."""
        llm_output_guard = AzureChatOpenAI(
            azure_endpoint=self.config.azure_endpoint,
            api_key=self.config.azure_api_key,
            azure_deployment=self.config.azure_deployment,
            api_version=self.config.azure_api_version,
            temperature=0
        )
        structured_llm_output_guard = llm_output_guard.with_structured_output(GuardrailOutput)

        output_guard_prompt = ChatPromptTemplate.from_messages([
            ("system", OutputGuardrailPrompts.SYSTEM_PROMPT),
            ("human", "User question: {question}\n\nGenerated response: {generation}"),
        ])

        return output_guard_prompt | structured_llm_output_guard
    
    def check(self, question: str, generation: str) -> GuardrailOutput:
        """Check if a generated response passes safety guardrails."""
        return self.guardrail.invoke({"question": question, "generation": generation})