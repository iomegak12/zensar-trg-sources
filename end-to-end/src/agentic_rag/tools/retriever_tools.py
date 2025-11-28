from typing import List
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import AzureOpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.tools import create_retriever_tool
from ..config import Config
from ..prompts import ToolDescriptions


class VectorStoreRetrieverTool:
    """Vector store retriever tool that loads multiple URLs."""
    
    def __init__(self, config: Config):
        self.config = config
        self._tool = None
        self._vectorstore = None
    
    @property
    def tool(self):
        if self._tool is None:
            self._tool = self._create_retriever_tool()
        return self._tool
    
    def _create_retriever_tool(self):
        """Create the retriever tool with vector store from multiple URLs."""
        # Get URLs to load
        urls = self.config.get_vector_store_urls()
        print(f"Loading documents from {len(urls)} URL(s)...")
        
        # Load documents from all URLs
        all_documents = []
        for url in urls:
            try:
                print(f"Loading: {url}")
                loader = WebBaseLoader(url)
                docs = loader.load()
                all_documents.extend(docs)
                print(f"✓ Loaded {len(docs)} documents from {url}")
            except Exception as e:
                print(f"✗ Failed to load {url}: {e}")
        
        if not all_documents:
            raise ValueError("Failed to load any documents from the provided URLs")
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        documents = text_splitter.split_documents(all_documents)
        print(f"Split into {len(documents)} chunks")
        
        # Create embeddings
        embeddings = AzureOpenAIEmbeddings(
            azure_endpoint=self.config.azure_endpoint,
            api_key=self.config.azure_api_key,
            azure_deployment=self.config.azure_embedding_deployment,
            api_version=self.config.azure_api_version
        )
        
        # Create vector store
        self._vectorstore = FAISS.from_documents(documents, embeddings)
        retriever = self._vectorstore.as_retriever()
        
        # Create retriever tool
        return create_retriever_tool(
            retriever,
            "knowledge_base_search",
            ToolDescriptions.KNOWLEDGE_BASE_SEARCH
        )