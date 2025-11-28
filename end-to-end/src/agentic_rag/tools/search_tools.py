from langchain_community.tools import WikipediaQueryRun, ArxivQueryRun
from langchain_community.utilities import WikipediaAPIWrapper, GoogleSerperAPIWrapper, ArxivAPIWrapper
from langchain_core.tools import tool
from ..config import Config
from ..prompts import ToolDescriptions


class GoogleSearchTool:
    """Google Search tool using Serper API."""
    
    def __init__(self, config: Config):
        self.config = config
        self._tool = None
    
    @property
    def tool(self):
        if self._tool is None:
            if not self.config.google_serper_api_key:
                raise ValueError("Google Serper API key not configured")
            self._tool = self._create_search_tool()
        return self._tool
    
    def _create_search_tool(self):
        @tool("GoogleSearch")
        def search(query_string: str):
            """Tool for searching the internet using Google Serper API."""
            search_tool = GoogleSerperAPIWrapper()
            return search_tool.run(query_string)
        
        # Update description from constants
        search.description = ToolDescriptions.GOOGLE_SEARCH
        return search


class WikipediaSearchTool:
    """Wikipedia search tool."""
    
    def __init__(self, config: Config):
        self.config = config
        self._tool = None
    
    @property
    def tool(self):
        if self._tool is None:
            self._tool = self._create_wikipedia_tool()
        return self._tool
    
    def _create_wikipedia_tool(self):
        api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=1000)
        return WikipediaQueryRun(
            name="WikipediaSearch",
            description=ToolDescriptions.WIKIPEDIA_SEARCH,
            api_wrapper=api_wrapper
        )


class ArxivSearchTool:
    """Arxiv academic paper search tool."""
    
    def __init__(self, config: Config):
        self.config = config
        self._tool = None
    
    @property
    def tool(self):
        if self._tool is None:
            self._tool = self._create_arxiv_tool()
        return self._tool
    
    def _create_arxiv_tool(self):
        arxiv_wrapper = ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=1000)
        return ArxivQueryRun(api_wrapper=arxiv_wrapper)