"""
Vector indexing functionality for chat data.

This module provides classes and functions for indexing chat data using
sentence transformers and ChromaDB. It handles chunking, embedding generation,
and storage of chat messages for semantic search.
"""

import uuid
import logging
from typing import Any, Dict, List, Optional

import chromadb
from config.settings import SENTENCE_TRANSFORMER_MODEL, VECTOR_STORE_PATH
from sentence_transformers import SentenceTransformer

# Set up logging
logger = logging.getLogger(__name__)

from src.utils.text_utils import chunk_messages, filter_complex_metadata


class VectorIndexer:
    """
    Class for indexing chat data using sentence transformers and ChromaDB.

    This class handles the process of converting chat messages into vector embeddings
    and storing them in a ChromaDB collection for efficient semantic search.
    It uses the SentenceTransformer model to generate embeddings for text chunks.
    """

    def __init__(self, model_name: str = SENTENCE_TRANSFORMER_MODEL,
                 vector_store_path: str = VECTOR_STORE_PATH):
        """
        Initialize the vector indexer with a model and database.

        Args:
            model_name (str): Name of the sentence transformer model to use.
            vector_store_path (str): Path to the ChromaDB vector store.
        """
        self.model_name = model_name
        self.vector_store_path = vector_store_path

        # Initialize the sentence transformer model
        self.model = SentenceTransformer(model_name)

        # Initialize the ChromaDB client
        # Use the settings from the configuration
        self.client = chromadb.PersistentClient(path=vector_store_path)
        logger.info(f"Initialized ChromaDB client with path: {vector_store_path}")

    def index_chat(self, chat_data: List[Dict[str, Any]], chat_id: Optional[str] = None) -> str:
        """
        Index chat data by chunking, embedding, and storing in ChromaDB.

        Args:
            chat_data (List[Dict[str, Any]]): List of message dictionaries.
            chat_id (Optional[str]): Unique identifier for the chat. If None, a UUID will be generated.

        Returns:
            str: The chat_id used for indexing.
        """
        # Generate a chat_id if not provided
        if chat_id is None:
            chat_id = str(uuid.uuid4())

        # Create or get the collection for this chat
        collection = self.client.get_or_create_collection(
            name=f"chat_{chat_id}",
            metadata={"chat_id": chat_id}
        )

        # Chunk the messages
        chunks_with_metadata = chunk_messages(chat_data)

        # Prepare data for batch insertion
        documents = []
        metadatas = []
        ids = []

        for i, (chunk, metadata) in enumerate(chunks_with_metadata):
            # Generate a unique ID for this chunk
            chunk_id = f"{chat_id}_{i}"

            # Filter metadata to ensure compatibility with vector stores
            filtered_metadata = filter_complex_metadata(metadata)

            documents.append(chunk)
            metadatas.append(filtered_metadata)
            ids.append(chunk_id)

        # Generate embeddings and add to the collection
        if documents:
            # Generate embeddings using the initialized model
            embeddings = self.model.encode(documents).tolist()
            collection.add(
                documents=documents,
                embeddings=embeddings, # Pass the generated embeddings
                metadatas=metadatas,
                ids=ids
            )

        return chat_id

    def get_collection_names(self) -> List[str]:
        """
        Get the names of all collections in the database.

        Returns:
            List[str]: List of collection names.
        """
        collections = self.client.list_collections()
        return [collection.name for collection in collections]


# Module-level functions that use a singleton instance of VectorIndexer
# This pattern ensures we only create one instance of the indexer
# to avoid loading the model multiple times and improve performance

_indexer = None

def _get_indexer() -> VectorIndexer:
    """
    Get or create a singleton instance of VectorIndexer.

    This internal function ensures we only create one instance of the VectorIndexer
    class, which helps with performance since loading embedding models can be expensive.

    Returns:
        VectorIndexer: The singleton instance.
    """
    global _indexer
    if _indexer is None:
        _indexer = VectorIndexer()
    return _indexer

def index_chat(chat_data: List[Dict[str, Any]], chat_id: Optional[str] = None) -> str:
    """
    Index chat data using the singleton VectorIndexer.

    Args:
        chat_data (List[Dict[str, Any]]): List of message dictionaries.
        chat_id (Optional[str]): Unique identifier for the chat.

    Returns:
        str: The chat_id used for indexing.
    """
    indexer = _get_indexer()
    return indexer.index_chat(chat_data, chat_id)

def get_collection_names() -> List[str]:
    """
    Get the names of all collections using the singleton VectorIndexer.

    Returns:
        List[str]: List of collection names.
    """
    indexer = _get_indexer()
    return indexer.get_collection_names()
