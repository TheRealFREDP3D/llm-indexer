"""
Markdown parser for chat logs.
"""

import re
from typing import List, Dict, Any
from datetime import datetime

from src.parsing.base_parser import BaseParser


class MarkdownParser(BaseParser):
    """
    Parser for chat logs in Markdown format.
    Expects a format where each message starts with a header (e.g., '## User:' or '## Assistant:')
    followed by the message content.
    """
    
    def __init__(self, user_pattern: str = r"##\s*User:?", assistant_pattern: str = r"##\s*Assistant:?"):
        """
        Initialize the Markdown parser with patterns for identifying message roles.
        
        Args:
            user_pattern (str): Regex pattern to identify user messages
            assistant_pattern (str): Regex pattern to identify assistant messages
        """
        self.user_pattern = user_pattern
        self.assistant_pattern = assistant_pattern
        
        # Combined pattern to split the content into messages
        self.split_pattern = f"({user_pattern}|{assistant_pattern})"
    
    def parse(self, content: str) -> List[Dict[str, Any]]:
        """
        Parse Markdown chat log content into a standardized format.
        
        Args:
            content (str): The raw Markdown content of the chat log.
            
        Returns:
            List[Dict[str, Any]]: A list of standardized message dictionaries.
        """
        # Split the content by headers to get individual messages
        parts = re.split(self.split_pattern, content, flags=re.MULTILINE)
        
        # Filter out empty parts and process
        parts = [p.strip() for p in parts if p.strip()]
        
        standardized_messages = []
        
        # Process parts in pairs (header + content)
        i = 0
        while i < len(parts) - 1:
            header = parts[i]
            message_content = parts[i + 1]
            
            # Determine the role based on the header
            if re.match(self.user_pattern, header, re.IGNORECASE):
                role = "user"
            elif re.match(self.assistant_pattern, header, re.IGNORECASE):
                role = "assistant"
            else:
                role = "unknown"
            
            # Extract timestamp if present in the header
            timestamp_match = re.search(r"\((\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z?)\)", header)
            timestamp = None
            if timestamp_match:
                try:
                    timestamp_str = timestamp_match.group(1)
                    timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                except ValueError:
                    pass
            
            # Create standardized message
            std_message = {
                "role": role,
                "content": message_content.strip()
            }
            
            # Add timestamp if available
            if timestamp:
                std_message["timestamp"] = timestamp
            
            standardized_messages.append(std_message)
            
            # Move to the next pair
            i += 2
        
        return standardized_messages
