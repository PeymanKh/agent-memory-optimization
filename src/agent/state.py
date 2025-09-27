"""
State Management Module

Defines the state structure for conversational agent memory management.
This module contains the TypedDict definition that manages message history
and conversation summaries.

Author: Peyman Kh
Last Update: 27-09-2025
"""
# Import libraries
from typing_extensions import TypedDict, Annotated, Optional
from langgraph.graph import add_messages
from langchain_core.messages import AnyMessage


class State(TypedDict):
    """
    State schema for the conversational agent workflow.

    Attributes:
        messages: List of conversation messages with automatic message handling
        summary: Optional cumulative summary of the conversation history
    """
    messages: Annotated[list[AnyMessage], add_messages]
    summary: Optional[str]
