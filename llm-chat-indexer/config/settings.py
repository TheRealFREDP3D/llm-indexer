"""
Configuration settings for the LLM Chat Indexer application.

This module provides access to configuration settings through the Configuration class.
It exports the configuration values as module-level variables for backward compatibility.

For new code, it's recommended to use the Configuration class directly:
    from config.config import config
    value = config.get('SETTING_NAME')
"""

from pathlib import Path

# Import the Configuration class
from config.config import config

# Export configuration values as module-level variables for backward compatibility

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Data storage paths
VECTOR_STORE_PATH = config.VECTOR_STORE_PATH
KG_PATH = config.KG_PATH

# API Keys
GEMINI_API_KEY = config.GEMINI_API_KEY

# Application constants
SENTENCE_TRANSFORMER_MODEL = config.SENTENCE_TRANSFORMER_MODEL
CHUNK_SIZE = config.CHUNK_SIZE
CHUNK_OVERLAP = config.CHUNK_OVERLAP
TOP_K_RESULTS = config.TOP_K_RESULTS

# ChromaDB settings
CHROMA_SETTINGS = config.CHROMA_SETTINGS
CHROMA_SERVER_SETTINGS = config.CHROMA_SERVER_SETTINGS

# ChromaDB server configuration
CHROMA_SERVER_HOST = config.CHROMA_SERVER_HOST
CHROMA_SERVER_HTTP_PORT = config.CHROMA_SERVER_HTTP_PORT
ALLOW_RESET = config.ALLOW_RESET
