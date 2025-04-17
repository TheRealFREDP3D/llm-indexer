"""
Semantic search functionality for chat data.

This module provides classes and functions for performing semantic search
on indexed chat data using sentence transformers and ChromaDB. It allows
searching within specific chats or across all indexed chats.
"""

from typing import List, Dict, Any

import chromadb
from sentence_transformers import SentenceTransformer

from config.settings import VECTOR_STORE_PATH, SENTENCE_TRANSFORMER_MODEL, TOP_K_RESULTS


class SemanticSearcher:
    """
    Class for semantic search of indexed chat data.

    This class provides methods to search for relevant content in indexed chat data
    using semantic similarity. It can search within a specific chat collection or
    across all available collections. The search is powered by sentence transformers
    and ChromaDB for vector similarity search.
    """

    def __init__(self, model_name: str = SENTENCE_TRANSFORMER_MODEL,
                 vector_store_path: str = VECTOR_STORE_PATH):
        """
        Initialize the semantic searcher with a model and database.

        Args:
            model_name (str): Name of the sentence transformer model to use.
            vector_store_path (str): Path to the ChromaDB vector store.
        """
        self.model_name = model_name
        self.vector_store_path = vector_store_path

        # Initialize the sentence transformer model
        self.model = SentenceTransformer(model_name)

        # Initialize the ChromaDB client
        self.client = chromadb.PersistentClient(path=vector_store_path)

    def search(self, query: str, chat_id: str, top_n: int = TOP_K_RESULTS) -> List[Dict[str, Any]]:
        """
        Search for relevant chunks in a specific chat collection.

        Args:
            query (str): The search query.
            chat_id (str): The ID of the chat to search in.
            top_n (int): Number of results to return.

        Returns:
            List[Dict[str, Any]]: List of search results with text and metadata.

        Raises:
            ValueError: If the chat collection doesn't exist.
        """
        collection_name = f"chat_{chat_id}"

        try:
            # Get the collection
            collection = self.client.get_collection(name=collection_name)

            # Query the collection
            results = collection.query(
                query_texts=[query],
                n_results=top_n
            )

            # Format the results
            formatted_results = []

            if results and results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    result = {
                        'text': doc,
                        'metadata': results['metadatas'][0][i] if results['metadatas'] and results['metadatas'][0] else {},
                        'distance': results['distances'][0][i] if results['distances'] and results['distances'][0] else None,
                        'id': results['ids'][0][i] if results['ids'] and results['ids'][0] else None
                    }
                    formatted_results.append(result)

            return formatted_results

        except Exception as e:
            # Properly raise from the original exception for better debugging
            raise ValueError(f"Error searching chat {chat_id}: {str(e)}") from e

    def search_all_collections(self, query: str, top_n: int = TOP_K_RESULTS) -> Dict[str, List[Dict[str, Any]]]:
        """
        Search for relevant chunks across all chat collections.

        Args:
            query (str): The search query.
            top_n (int): Number of results to return per collection.

        Returns:
            Dict[str, List[Dict[str, Any]]]: Dictionary mapping chat_ids to search results.
        """
        # Get all collections
        collections = self.client.list_collections()

        # Search each collection
        results_by_chat = {}

        for collection in collections:
            # Extract chat_id from collection name
            if collection.name.startswith("chat_"):
                chat_id = collection.name[5:]  # Remove "chat_" prefix

                try:
                    # Search this collection and add to results if not empty
                    if results := self.search(query, chat_id, top_n):
                        results_by_chat[chat_id] = results
                except Exception:
                    # Skip collections that cause errors
                    continue

        return results_by_chat


# Module-level functions that use a singleton instance of SemanticSearcher
# This pattern ensures we only create one instance of the searcher
# to avoid loading the model multiple times and improve performance

_searcher = None

def _get_searcher() -> SemanticSearcher:
    """
    Get or create a singleton instance of SemanticSearcher.

    This internal function ensures we only create one instance of the SemanticSearcher
    class, which helps with performance since loading embedding models can be expensive.

    Returns:
        SemanticSearcher: The singleton instance.
    """
    global _searcher
    if _searcher is None:
        _searcher = SemanticSearcher()
    return _searcher

def search(query: str, chat_id: str, top_n: int = TOP_K_RESULTS) -> List[Dict[str, Any]]:
    """
    Search for relevant chunks in a specific chat collection using the singleton SemanticSearcher.

    Args:
        query (str): The search query.
        chat_id (str): The ID of the chat to search in.
        top_n (int): Number of results to return.

    Returns:
        List[Dict[str, Any]]: List of search results with text and metadata.
    """
    searcher = _get_searcher()
    return searcher.search(query, chat_id, top_n)

def search_all_collections(query: str, top_n: int = TOP_K_RESULTS) -> Dict[str, List[Dict[str, Any]]]:
    """
    Search for relevant chunks across all chat collections using the singleton SemanticSearcher.

    Args:
        query (str): The search query.
        top_n (int): Number of results to return per collection.

    Returns:
        Dict[str, List[Dict[str, Any]]]: Dictionary mapping chat_ids to search results.
    """
    searcher = _get_searcher()
    return searcher.search_all_collections(query, top_n)
