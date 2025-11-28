from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from ..config import Config
from ..prompts import QuestionRewriterPrompts


class QuestionRewriter:
    """Question rewriter for improved retrieval."""
    
    def __init__(self, config: Config):
        self.config = config
        self._rewriter = None
    
    @property
    def rewriter(self):
        if self._rewriter is None:
            self._rewriter = self._create_question_rewriter()
        return self._rewriter
    
    def _create_question_rewriter(self):
        """Create the question rewriter chain."""
        llm_rewriter = AzureChatOpenAI(
            azure_endpoint=self.config.azure_endpoint,
            api_key=self.config.azure_api_key,
            azure_deployment=self.config.azure_deployment,
            api_version=self.config.azure_api_version,
            temperature=0
        )

        re_write_prompt = ChatPromptTemplate.from_messages([
            ("system", QuestionRewriterPrompts.SYSTEM_PROMPT),
            ("human", "Here is the initial question: \n\n {question} \n Formulate an improved question."),
        ])

        return re_write_prompt | llm_rewriter | StrOutputParser()
    
    def rewrite(self, question: str) -> str:
        """Rewrite a question for better retrieval."""
        return self.rewriter.invoke({"question": question})