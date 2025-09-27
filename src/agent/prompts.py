"""
Prompt Templates Module

Contains all prompt templates used throughout the conversational agent workflow.
This module centralizes prompt management for consistent messaging and
easy template modifications.

Author: Peyman Kh
Last Update: 27-09-2025
"""
# Import libraries
from langchain_core.prompts import PromptTemplate


assistant_system_message = PromptTemplate(
    input_variables=["summary"],
    template="""You are a helpful assistant. You are given a conversation history and a summary of the conversation so far. Your task is to respond to the user's message.\n\nsummary of conversations so far: ``````"""
)


summary_update_template = PromptTemplate(
    input_variables=["existing_summary", "new_messages"],
    template="""You are tasked with updating a conversation summary.

EXISTING SUMMARY:
{existing_summary}

NEW MESSAGES SINCE LAST SUMMARY:
{new_messages}

INSTRUCTIONS:
1. Keep ALL important information from the existing summary
2. Add new relevant information from the recent messages
3. Create a comprehensive, cumulative summary that includes both old and new context
4. Do not lose any important details from the previous summary

Updated Summary:"""
)

summary_initial_template = PromptTemplate(
    input_variables=["messages"],
    template="""Create a comprehensive summary of this conversation:

MESSAGES:
{messages}

Summary:"""
)
