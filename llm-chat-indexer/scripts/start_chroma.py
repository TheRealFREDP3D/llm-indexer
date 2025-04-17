"""
Script to start the ChromaDB server.

This script starts a ChromaDB server using the Server API.
It uses the configuration from config.py.
"""

import os
import logging

import chromadb
from chromadb.config import Settings

# Import configuration
from config.config import config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Ensure the vector store directory exists
os.makedirs(config.VECTOR_STORE_PATH, exist_ok=True)

def main():
    """Run the ChromaDB server."""
    logger.info(f"Starting ChromaDB server with data directory: {config.VECTOR_STORE_PATH}")

    # Configure the server using settings from config
    settings = Settings(
        chroma_api_impl="rest",
        chroma_server_host=config.CHROMA_SERVER_HOST,
        chroma_server_http_port=config.CHROMA_SERVER_HTTP_PORT,
        allow_reset=config.ALLOW_RESET
    )

    # Start the server
    logger.info(f"Starting ChromaDB server on {config.CHROMA_SERVER_HOST}:{config.CHROMA_SERVER_HTTP_PORT}")
    server = chromadb.Server(settings)

    try:
        server.run()
    except KeyboardInterrupt:
        logger.info("ChromaDB server stopped by user")

if __name__ == "__main__":
    main()