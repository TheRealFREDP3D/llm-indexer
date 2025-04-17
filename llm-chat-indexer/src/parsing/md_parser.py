"""
Markdown parser for chat logs.
"""

import re
from typing import List, Dict, Any, Optional
from datetime import datetime

from src.parsing.base_parser import BaseParser


class MarkdownParser(BaseParser):
    """
    Parser for chat logs in Markdown format.
    Expects a format where each message starts with a header (e.g., '## User:' or '## Assistant:')
    followed by the message content.
    """

    def __init__(self, user_patterns: Optional[List[str]] = None, assistant_patterns: Optional[List[str]] = None):
        """
        Initialize the Markdown parser with patterns for identifying message roles.

        Args:
            user_patterns (list): List of regex patterns to identify user messages
            assistant_patterns (list): List of regex patterns to identify assistant messages
        """
        # Default patterns for user and assistant messages
        if user_patterns is None:
            user_patterns = [r"##\s*User:?", r"\*\*User\*\*:?", r"#\s*User:?"]
        if assistant_patterns is None:
            assistant_patterns = [r"##\s*Assistant:?", r"\*\*Assistant\*\*:?", r"#\s*Assistant:?"]

        self.user_patterns = user_patterns
        self.assistant_patterns = assistant_patterns

    def parse(self, content: str) -> List[Dict[str, Any]]:
        """
        Parse Markdown chat log content into a standardized format.

        Args:
            content (str): The raw Markdown content of the chat log.

        Returns:
            List[Dict[str, Any]]: A list of standardized message dictionaries.
        """
        standardized_messages = []

        # Try different patterns to find messages
        # First, try to find user messages
        user_matches = []
        for pattern in self.user_patterns:
            for match in re.finditer(pattern, content, re.MULTILINE | re.IGNORECASE):
                user_matches.append((match.start(), "user", match.group()))

        # Then, try to find assistant messages
        assistant_matches = []
        for pattern in self.assistant_patterns:
            for match in re.finditer(pattern, content, re.MULTILINE | re.IGNORECASE):
                assistant_matches.append((match.start(), "assistant", match.group()))

        # Combine and sort all matches by position
        all_matches = sorted(user_matches + assistant_matches, key=lambda x: x[0])

        # Process matches to extract content
        for i in range(len(all_matches)):
            current_match = all_matches[i]
            role = current_match[1]
            header = current_match[2]

            # Determine the content boundaries
            start_pos = current_match[0] + len(header)
            end_pos = len(content)
            if i < len(all_matches) - 1:
                end_pos = all_matches[i + 1][0]

            # Extract the content
            message_content = content[start_pos:end_pos].strip()

            # Skip empty content
            if not message_content:
                continue

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

            # No need to increment a counter in the new approach

        return standardized_messages
