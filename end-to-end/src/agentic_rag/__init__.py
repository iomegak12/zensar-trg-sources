"""
Agentic Self-Reflective RAG Package

A production-ready RAG system with multi-tool routing, quality grading,
and comprehensive guardrails using LangGraph and Azure OpenAI.
"""

from .main import AgenticRAG

__version__ = "1.0.0"
__all__ = ["AgenticRAG"]