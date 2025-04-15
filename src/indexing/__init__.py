"""
Indexing module for LLM Chat Indexer.
Contains functionality for embedding and storing chat data.
"""

from src.indexing.vector_indexer import index_chat, get_collection_names

__all__ = ['index_chat', 'get_collection_names']
