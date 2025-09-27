"""
Graph Tools Module

Implements Tavily search tool for the assistant so that it can search the web
for information about the topic of the conversation.

Author: Peyman Kh
Last Update: 27-09-2025
"""
# Import libraries
from langchain_core.tools import tool
from langchain_tavily import TavilySearch

from src.config.config import config


@tool("web_search", description="Search the web for information about the question asked.")
def web_search(question: str):
    """
    Search the web for information about the question asked.

    Args:
        question (str): The question to search the web for.
    """

    tavily_search = TavilySearch(tavily_api_key=config.llm.tavily_api_key.get_secret_value(), max_results=3)
    search_docs = tavily_search.invoke(question)

    return search_docs
