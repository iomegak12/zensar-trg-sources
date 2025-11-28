from setuptools import setup, find_packages

setup(
    name="agentic_rag",
    version="1.0.0",
    description="Agentic Self-Reflective RAG system with LangGraph and Azure OpenAI",
    author="Zensar AI Team",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "langchain>=0.1.0",
        "langchain-openai>=0.1.0",
        "langchain-community>=0.1.0",
        "langgraph>=0.1.0",
        "faiss-cpu>=1.7.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.0.0",
        "beautifulsoup4>=4.12.0",
        "requests>=2.31.0",
    ],
    extras_require={
        "dev": ["pytest", "black", "flake8"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)