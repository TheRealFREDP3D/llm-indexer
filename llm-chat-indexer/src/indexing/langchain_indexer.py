"""
LangChain-based indexing functionality for chat data.
"""

from pathlib import Path
from typing import Any, Dict, List

import chromadb
from config.settings import (
    CHROMA_SETTINGS,
    SENTENCE_TRANSFORMER_MODEL,
    VECTOR_STORE_PATH,
)
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores.utils import filter_complex_metadata

from src.utils.text_utils import filter_complex_metadata as custom_filter_metadata


class LangChainIndexer:
    """
    Class for indexing chat data using LangChain.
    """

    def __init__(self, model_name: str = SENTENCE_TRANSFORMER_MODEL,
                 vector_store_path: str = VECTOR_STORE_PATH):
        """
        Initialize the LangChain indexer with a model and database.

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

    def _prepare_documents(self, chat_data: List[Dict[str, Any]]) -> List[Document]:
        """
        Convert chat messages into LangChain documents.

        Args:
            chat_data (List[Dict[str, Any]]): List of chat messages.

        Returns:
            List[Document]: List of LangChain documents.
        """
        documents = []

        for i, message in enumerate(chat_data):
            # Create metadata dictionary
            metadata = {
                'role': message.get('role', 'unknown'),
                'timestamp': message.get('timestamp', None),
                'message_id': message.get('id', str(i)),
                'index': i
            }

            # Add any additional fields from the original message
            for key, value in message.items():
                if key not in ['role', 'content', 'timestamp', 'id']:
                    metadata[key] = value

            # Filter metadata to ensure compatibility with vector stores
            filtered_metadata = custom_filter_metadata(metadata)

            # Create a document for each message
            doc = Document(
                page_content=message['content'],
                metadata=filtered_metadata
            )
            documents.append(doc)

        # Split documents into chunks
        split_docs = self.text_splitter.split_documents(documents)
        return split_docs

    def index_chat(self, chat_data: List[Dict[str, Any]], chat_id: str) -> None:
        """
        Index a chat conversation.

        Args:
            chat_data (List[Dict[str, Any]]): List of chat messages.
            chat_id (str): Unique identifier for the chat.
        """
        collection_path = self._get_collection_path(chat_id)

        # Prepare documents
        documents = self._prepare_documents(chat_data)

        # Filter complex metadata from documents
        filtered_documents = filter_complex_metadata(documents)

        # Create and persist the vector store
        vectorstore = Chroma.from_documents(
            documents=filtered_documents,
            embedding=self.embedding_function,
            persist_directory=str(collection_path)
        )
        vectorstore.persist()

    def get_collection_names(self) -> List[str]:
        """
        Get a list of all indexed chat collection names.

        Returns:
            List[str]: List of collection names (with 'chat_' prefix).
        """
        collections = []
        for path in self.vector_store_path.glob("chat_*"):
            if path.is_dir():
                collections.append(path.name)
        return collections


# Module-level functions that use a singleton instance of LangChainIndexer

_indexer = None

def _get_indexer() -> LangChainIndexer:
    """
    Get or create a singleton instance of LangChainIndexer.

    Returns:
        LangChainIndexer: The singleton instance.
    """
    global _indexer
    if _indexer is None:
        _indexer = LangChainIndexer()
    return _indexer

def index_chat(chat_data: List[Dict[str, Any]], chat_id: str) -> None:
    """
    Index a chat conversation using the singleton LangChainIndexer.

    Args:
        chat_data (List[Dict[str, Any]]): List of chat messages.
        chat_id (str): Unique identifier for the chat.
    """
    indexer = _get_indexer()
    indexer.index_chat(chat_data, chat_id)

def get_collection_names() -> List[str]:
    """
    Get a list of all indexed chat collection names using the singleton LangChainIndexer.

    Returns:
        List[str]: List of collection names (with 'chat_' prefix).
    """
    indexer = _get_indexer()
    return indexer.get_collection_names()