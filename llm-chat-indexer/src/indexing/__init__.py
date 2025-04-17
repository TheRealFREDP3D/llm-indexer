"""
Indexing functionality for chat data.
"""

from .langchain_indexer import get_collection_names, index_chat

__all__ = ['index_chat', 'get_collection_names']
