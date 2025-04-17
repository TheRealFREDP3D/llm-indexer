"""
LangChain-based semantic search functionality for chat data.
"""

from pathlib import Path
from typing import Any, Dict, List

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma

from config.settings import (
    SENTENCE_TRANSFORMER_MODEL,
    TOP_K_RESULTS,
    VECTOR_STORE_PATH,
)


class LangChainSearcher:
    """
    Class for semantic search of indexed chat data using LangChain.
    """
    
    def __init__(self, model_name: str = SENTENCE_TRANSFORMER_MODEL, 
                 vector_store_path: str = VECTOR_STORE_PATH):
        """
        Initialize the LangChain searcher with a model and database.
        
        Args:
            model_name (str): Name of the sentence transformer model to use.
            vector_store_path (str): Path to the ChromaDB vector store.
        """
        self.model_name = model_name
        self.vector_store_path = Path(vector_store_path)
        
        # Initialize the embedding function
        self.embedding_function = SentenceTransformerEmbeddings(model_name=model_name)
        
        # Initialize the text splitter for document chunking
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
    
    def _get_collection_path(self, chat_id: str) -> Path:
        """Get the path for a specific chat collection."""
        return self.vector_store_path / f"chat_{chat_id}"
    
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
        collection_path = self._get_collection_path(chat_id)
        
        try:
            # Load the vector store
            vectorstore = Chroma(
                persist_directory=str(collection_path),
                embedding_function=self.embedding_function
            )
            
            # Perform the search
            results = vectorstore.similarity_search_with_score(query, k=top_n)
            
            # Format the results
            formatted_results = []
            for doc, score in results:
                result = {
                    'text': doc.page_content,
                    'metadata': doc.metadata,
                    'distance': score,
                    'id': doc.metadata.get('id', None)
                }
                formatted_results.append(result)
            
            return formatted_results
            
        except Exception as e:
            raise ValueError(f"Error searching chat {chat_id}: {str(e)}")
    
    def search_all_collections(self, query: str, top_n: int = TOP_K_RESULTS) -> Dict[str, List[Dict[str, Any]]]:
        """
        Search for relevant chunks across all chat collections.
        
        Args:
            query (str): The search query.
            top_n (int): Number of results to return per collection.
            
        Returns:
            Dict[str, List[Dict[str, Any]]]: Dictionary mapping chat_ids to search results.
        """
        results_by_chat = {}
        
        # Search through all subdirectories in the vector store path
        for collection_path in self.vector_store_path.glob("chat_*"):
            if collection_path.is_dir():
                # Extract chat_id from directory name
                chat_id = collection_path.name[5:]  # Remove "chat_" prefix
                
                try:
                    # Search this collection
                    results = self.search(query, chat_id, top_n)
                    
                    # Add to results if not empty
                    if results:
                        results_by_chat[chat_id] = results
                except Exception:
                    # Skip collections that cause errors
                    continue
        
        return results_by_chat


# Module-level functions that use a singleton instance of LangChainSearcher

_searcher = None

def _get_searcher() -> LangChainSearcher:
    """
    Get or create a singleton instance of LangChainSearcher.
    
    Returns:
        LangChainSearcher: The singleton instance.
    """
    global _searcher
    if _searcher is None:
        _searcher = LangChainSearcher()
    return _searcher

def search(query: str, chat_id: str, top_n: int = TOP_K_RESULTS) -> List[Dict[str, Any]]:
    """
    Search for relevant chunks in a specific chat collection using the singleton LangChainSearcher.
    
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
    Search for relevant chunks across all chat collections using the singleton LangChainSearcher.
    
    Args:
        query (str): The search query.
        top_n (int): Number of results to return per collection.
        
    Returns:
        Dict[str, List[Dict[str, Any]]]: Dictionary mapping chat_ids to search results.
    """
    searcher = _get_searcher()
    return searcher.search_all_collections(query, top_n) 