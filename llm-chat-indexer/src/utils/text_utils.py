"""
Text utility functions for cleaning and chunking text.

This module provides utility functions for processing text data before indexing,
including cleaning text by removing extra whitespace and normalizing line breaks,
chunking text into smaller segments for embedding, and processing chat messages
into chunks with associated metadata.
"""

import re
from typing import List, Dict, Any, Tuple, Union

from config.settings import CHUNK_SIZE, CHUNK_OVERLAP


def clean_text(text: str) -> str:
    """
    Clean text by removing extra whitespace, normalizing line breaks, etc.

    Args:
        text (str): The text to clean.

    Returns:
        str: The cleaned text.
    """
    if not text:
        return ""

    # Replace multiple newlines with a single newline
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Replace multiple spaces with a single space
    text = re.sub(r' {2,}', ' ', text)

    # Strip leading/trailing whitespace
    text = text.strip()

    return text


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP) -> List[str]:
    """
    Split text into overlapping chunks for embedding.

    This function divides a long text into smaller, overlapping chunks suitable for
    embedding generation. It attempts to find natural breaking points like sentence
    boundaries when possible to create more meaningful chunks.

    Args:
        text (str): The text to chunk.
        chunk_size (int): The maximum size of each chunk in characters.
        chunk_overlap (int): The overlap between consecutive chunks in characters.

    Returns:
        List[str]: A list of text chunks.
    """
    if not text:
        return []

    # Clean the text first
    text = clean_text(text)

    # If text is shorter than chunk_size, return it as a single chunk
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        # Get a chunk of size chunk_size or the remaining text if shorter
        end = min(start + chunk_size, len(text))

        # If this is not the first chunk and not at the end of the text,
        # try to find a good breaking point (e.g., end of sentence)
        if start > 0 and end < len(text):
            # Look for sentence boundaries within the last 20% of the chunk
            search_start = max(start + int(chunk_size * 0.8), start)

            # Try to find the last sentence boundary
            last_period = text.rfind('. ', search_start, end)
            last_newline = text.rfind('\n', search_start, end)

            # Use the latest boundary found
            if last_period > search_start:
                end = last_period + 1  # Include the period
            elif last_newline > search_start:
                end = last_newline + 1  # Include the newline

        # Add the chunk to the list
        chunks.append(text[start:end])

        # Move the start position for the next chunk, considering overlap
        start = end - chunk_overlap

        # Ensure we're making progress
        start = min(start, end)

    return chunks


def filter_complex_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Filter out metadata values that are not supported by vector stores.

    Vector stores typically only support simple types like str, int, float, and bool.
    This function removes or converts complex types to ensure compatibility.

    Args:
        metadata (Dict[str, Any]): The metadata dictionary to filter.

    Returns:
        Dict[str, Any]: A filtered metadata dictionary with only compatible types.
    """
    filtered_metadata = {}

    for key, value in metadata.items():
        # Skip None values
        if value is None:
            continue

        # Keep simple types
        if isinstance(value, (str, int, float, bool)):
            filtered_metadata[key] = value
        # Convert other types to strings if possible
        else:
            try:
                filtered_metadata[key] = str(value)
            except:
                # Skip values that can't be converted to string
                pass

    return filtered_metadata


def chunk_messages(messages: List[Dict[str, Any]], chunk_size: int = CHUNK_SIZE,
                  chunk_overlap: int = CHUNK_OVERLAP) -> List[Tuple[str, Dict[str, Any]]]:
    """
    Process a list of messages and create chunks with metadata.

    This function takes a list of chat messages, formats them with role prefixes,
    chunks them into smaller segments, and attaches relevant metadata to each chunk.
    The metadata includes information about the original message such as role,
    timestamp, and position in the conversation.

    Args:
        messages (List[Dict[str, Any]]): List of message dictionaries with 'role' and 'content' keys.
        chunk_size (int): The maximum size of each chunk in characters.
        chunk_overlap (int): The overlap between consecutive chunks in characters.

    Returns:
        List[Tuple[str, Dict[str, Any]]]: A list of tuples containing:
            - The text chunk
            - Metadata dictionary with information about the original message(s)
    """
    chunks_with_metadata = []

    for i, message in enumerate(messages):
        role = message.get('role', 'unknown')
        content = message.get('content', '')

        # Skip empty messages
        if not content.strip():
            continue

        # Format the message with role prefix
        formatted_text = f"{role.capitalize()}: {content}"

        # Chunk the formatted text
        text_chunks = chunk_text(formatted_text, chunk_size, chunk_overlap)

        # Create metadata for each chunk
        for j, chunk in enumerate(text_chunks):
            metadata = {
                'message_index': i,
                'chunk_index': j,
                'total_chunks': len(text_chunks),
                'role': role,
                'timestamp': message.get('timestamp')
            }

            # Add any additional fields from the original message
            for key, value in message.items():
                if key not in ['role', 'content', 'timestamp']:
                    metadata[key] = value

            # Filter metadata to ensure compatibility with vector stores
            filtered_metadata = filter_complex_metadata(metadata)

            chunks_with_metadata.append((chunk, filtered_metadata))

    return chunks_with_metadata
