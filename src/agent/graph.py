"""
Workflow Graph Module

This module assembles the complete LangGraph workflow with nodes, edges,
and memory management capabilities.

Author: Peyman Kh
Last Update: 27-09-2025
"""
# Import libraries
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START, END

from src.agent.state import State
from src.agent.tools import web_search
from langgraph.prebuilt import ToolNode, tools_condition
from src.agent.nodes import assistant, summarize_conversation, router

from src.config.config import config


def create_llm():
    """
    Create and configure the language model instance with tools.

    Returns:
        ChatOpenAI: Configured language model instance
    """
    llm = ChatOpenAI(
        api_key=config.llm.api_key.get_secret_value(),
        model=config.llm.model_name
    )

    llm_with_tools = llm.bind_tools([web_search], parallel_tool_calls=False)

    return llm_with_tools


def build_workflow(llm):
    """
    Construct the conversational agent workflow graph.

    Args:
        llm: Language model instance to use in nodes

    Returns:
        CompiledGraph: Compiled workflow graph with memory checkpointer
    """
    # Create the workflow
    workflow = StateGraph(State)

    workflow.add_node("assistant", lambda state: assistant(state, llm))
    workflow.add_node("summarize_conversation", lambda state: summarize_conversation(state, llm))
    workflow.add_node("tools", ToolNode([web_search]))

    workflow.add_edge(START, "assistant")
    workflow.add_conditional_edges("assistant", tools_condition)
    workflow.add_edge("tools", "assistant")
    workflow.add_conditional_edges("assistant", router, ["summarize_conversation", END])
    workflow.add_edge("summarize_conversation", END)

    # Compile WITHOUT memory for LangGraph Studio
    return workflow.compile()


def build_workflow_with_memory(llm):
    """For local use with memory"""
    workflow = StateGraph(State)
    workflow.add_node("assistant", lambda state: assistant(state, llm))
    workflow.add_node("summarize_conversation", lambda state: summarize_conversation(state, llm))
    workflow.add_node("tools", ToolNode([web_search]))

    workflow.add_edge(START, "assistant")
    workflow.add_conditional_edges("assistant", tools_condition)
    workflow.add_edge("tools", "assistant")
    workflow.add_conditional_edges("assistant", router, ["summarize_conversation", END])
    workflow.add_edge("summarize_conversation", END)

    memory = InMemorySaver()
    return workflow.compile(checkpointer=memory)


# For LangGraph Studio
model = create_llm()
graph = build_workflow(model)
