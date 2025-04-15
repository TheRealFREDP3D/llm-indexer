"""
Distiller for generating summaries of chat data.
"""

from typing import List, Dict, Any, Optional

from src.llm_clients.gemini_client import GeminiClient


def format_messages_for_summary(messages: List[Dict[str, Any]]) -> str:
    """
    Format a list of messages into a string suitable for summarization.
    
    Args:
        messages (List[Dict[str, Any]]): List of message dictionaries.
        
    Returns:
        str: Formatted string representation of the conversation.
    """
    formatted_text = ""
    
    for message in messages:
        role = message.get('role', 'unknown')
        content = message.get('content', '')
        
        # Skip empty messages
        if not content.strip():
            continue
        
        # Add the message to the formatted text
        formatted_text += f"{role.capitalize()}: {content}\n\n"
    
    return formatted_text.strip()


def generate_summary(chat_data: List[Dict[str, Any]], summary_type: str = "gist") -> str:
    """
    Generate a summary of the chat data.
    
    Args:
        chat_data (List[Dict[str, Any]]): List of message dictionaries.
        summary_type (str): Type of summary to generate ('gist' or 'key_points').
        
    Returns:
        str: The generated summary.
        
    Raises:
        ValueError: If the summary type is not supported.
    """
    # Validate summary type
    if summary_type not in ["gist", "key_points"]:
        raise ValueError(f"Unsupported summary type: {summary_type}. Use 'gist' or 'key_points'.")
    
    # Format the messages for summarization
    formatted_text = format_messages_for_summary(chat_data)
    
    # If there's no content to summarize, return an empty string
    if not formatted_text:
        return ""
    
    # Initialize the Gemini client
    client = GeminiClient()
    
    # Generate the summary
    summary = client.generate_summary(formatted_text, summary_type)
    
    return summary
