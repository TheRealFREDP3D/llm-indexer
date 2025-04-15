"""
Base parser class for chat logs.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseParser(ABC):
    """
    Abstract base class for chat log parsers.
    All concrete parsers should inherit from this class and implement the parse method.
    """
    
    @abstractmethod
    def parse(self, content: str) -> List[Dict[str, Any]]:
        """
        Parse chat log content into a standardized format.
        
        Args:
            content (str): The raw content of the chat log.
            
        Returns:
            List[Dict[str, Any]]: A list of message dictionaries with standardized fields:
                - 'role': The role of the message sender (e.g., 'user', 'assistant')
                - 'content': The content of the message
                - 'timestamp': The timestamp of the message (if available)
                - Additional metadata fields may be included
        """
        pass
