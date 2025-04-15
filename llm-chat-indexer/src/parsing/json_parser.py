"""
JSON parser for chat logs.
"""

import json
from typing import List, Dict, Any
from datetime import datetime

from src.parsing.base_parser import BaseParser


class JSONParser(BaseParser):
    """
    Parser for chat logs in JSON format.
    Expects a JSON array of message objects.
    """
    
    def __init__(self, role_field: str = "role", content_field: str = "content", timestamp_field: str = "timestamp"):
        """
        Initialize the JSON parser with field mappings.
        
        Args:
            role_field (str): The field name for the message role in the JSON
            content_field (str): The field name for the message content in the JSON
            timestamp_field (str): The field name for the message timestamp in the JSON
        """
        self.role_field = role_field
        self.content_field = content_field
        self.timestamp_field = timestamp_field
    
    def parse(self, content: str) -> List[Dict[str, Any]]:
        """
        Parse JSON chat log content into a standardized format.
        
        Args:
            content (str): The raw JSON content of the chat log.
            
        Returns:
            List[Dict[str, Any]]: A list of standardized message dictionaries.
            
        Raises:
            ValueError: If the content is not valid JSON or doesn't contain a list of messages.
        """
        try:
            # Parse the JSON content
            data = json.loads(content)
            
            # Ensure data is a list
            if not isinstance(data, list):
                if isinstance(data, dict) and "messages" in data:
                    # Handle case where messages are in a 'messages' field
                    data = data["messages"]
                else:
                    raise ValueError("JSON content must be a list of messages or a dict with a 'messages' field")
            
            # Standardize each message
            standardized_messages = []
            for message in data:
                if not isinstance(message, dict):
                    continue
                
                # Extract fields with defaults
                role = message.get(self.role_field, "unknown")
                content = message.get(self.content_field, "")
                
                # Handle timestamp if present
                timestamp = message.get(self.timestamp_field)
                if timestamp:
                    # Try to parse timestamp to a standard format if it's a string
                    if isinstance(timestamp, str):
                        try:
                            timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        except ValueError:
                            # If parsing fails, keep the original string
                            pass
                
                # Create standardized message
                std_message = {
                    "role": role,
                    "content": content
                }
                
                # Add timestamp if available
                if timestamp:
                    std_message["timestamp"] = timestamp
                
                # Add any additional fields as metadata
                for key, value in message.items():
                    if key not in [self.role_field, self.content_field, self.timestamp_field]:
                        std_message[key] = value
                
                standardized_messages.append(std_message)
            
            return standardized_messages
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON content: {str(e)}")
