"""
Simple CLI for conversational agent with memory management.

Author: Peyman Kh
Last Update: 27-09-2025
"""
# Import libraries
import logging
from langchain_core.messages import HumanMessage

from src.agent.graph import create_llm, build_workflow

logging.disable(logging.CRITICAL)

def chat():
    """Run an interactive chat session."""

    # Create agent
    llm = create_llm()
    graph = build_workflow(llm)

    # Chat loop
    thread_config = {"configurable": {"thread_id": "chat-session"}}

    print("Chat with the agent (type 'quit' to exit):")

    while True:
        user_input = input("\nYou: ")

        if user_input.lower() in ['quit', 'exit']:
            break

        try:
            result = graph.invoke(
                {"messages": [HumanMessage(content=user_input)]},
                config=thread_config
            )

            response = result["messages"][-1].content
            print(f"Agent: {response}")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    chat()
