"""
Graph Nodes Module

This module contains the business logic for message processing, conversation
summarization, and routing decisions.

Author: Peyman Kh
Last Update: 27-09-2025
"""
# Import libraries
from langgraph.graph import END
from langchain_core.messages import SystemMessage, HumanMessage, RemoveMessage

from src.agent.state import State
from src.agent.prompts import assistant_system_message, summary_initial_template, summary_update_template


def assistant(state: State, llm):
    """
    Assistant node for responding to user messages.

    Creates a system message with conversation summary if available,
    then invokes the LLM to generate a response.

    Args:
        state: Current conversation state containing messages and summary
        llm: Language model instance for generating responses

    Returns:
        dict: Updated state with the assistant response message
    """
    # Get messages and summary if exists
    messages = state["messages"]
    summary = state.get("summary", "")

    # Create the system message with summary
    system_message = SystemMessage(content=assistant_system_message.format(summary=summary))

    # Invoke LLM
    response = llm.invoke([system_message] + messages)

    # Write response to state
    return {"messages": [response]}


def summarize_conversation(state: State, llm):
    """
    Conversation summarization node.

    Creates or updates a cumulative summary of the conversation history,
    then removes old messages to optimize memory usage while preserving
    the most recent context.

    Args:
        state: Current conversation state containing messages and summary
        llm: Language model instance for generating summaries

    Returns:
        dict: Updated state with new summary and pruned message history
    """
    # Get messages and existing summary
    messages = state["messages"]
    existing_summary = state.get("summary", "")

    # Format message content for the prompt
    message_contents = [message.content for message in messages]

    # Use the appropriate prompt template based on whether the summary exists
    if existing_summary:
        # Update existing summary
        summary_prompt = summary_update_template.format(
            existing_summary=existing_summary,
            new_messages=message_contents
        )
    else:
        # Create an initial summary
        summary_prompt = summary_initial_template.format(
            messages=message_contents
        )

    # Create the summarization request
    summary_messages = [HumanMessage(content=summary_prompt)]
    summary_response = llm.invoke(summary_messages)

    # Delete all but the 2 most recent messages
    delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]

    # Return the CUMULATIVE summary and deleted messages
    return {"summary": summary_response.content, "messages": delete_messages}


def router(state: State):
    """
    Routing node for workflow decision making.

    Determines the next step in the workflow based on message count.
    Triggers summarization when message threshold is exceeded.

    Args:
        state: Current conversation state containing messages

    Returns:
        str: Next node to execute ("summarize_conversation" or END)
    """
    # Check if there are any messages first
    if not state["messages"]:
        return "END"

    return "summarize_conversation" if len(state["messages"]) > 6 else END
