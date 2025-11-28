from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from ..config import Config
from ..prompts import AnswerGeneratorPrompts


class AnswerGenerator:
    """Answer generator for the RAG system."""
    
    def __init__(self, config: Config):
        self.config = config
        self._generator = None
    
    @property
    def generator(self):
        if self._generator is None:
            self._generator = self._create_generator()
        return self._generator
    
    def _create_generator(self):
        """Create the answer generation chain."""
        llm_generator = AzureChatOpenAI(
            azure_endpoint=self.config.azure_endpoint,
            api_key=self.config.azure_api_key,
            azure_deployment=self.config.azure_deployment,
            api_version=self.config.azure_api_version,
            temperature=0,
            max_tokens=2000
        )

        generation_prompt = ChatPromptTemplate.from_messages([
            ("system", AnswerGeneratorPrompts.SYSTEM_PROMPT),
            ("human", "Context: {context}\n\nQuestion: {question}\n\nProvide a comprehensive answer:")
        ])

        return generation_prompt | llm_generator | StrOutputParser()
    
    def generate(self, context: str, question: str) -> str:
        """Generate an answer based on context and question."""
        return self.generator.invoke({"context": context, "question": question})