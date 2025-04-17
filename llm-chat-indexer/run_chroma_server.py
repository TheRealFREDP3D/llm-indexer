#!/usr/bin/env python
"""
Script to run a ChromaDB server.

This script starts a ChromaDB server that the main application can connect to.
"""

import os
import logging
import time
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Get the base directory
BASE_DIR = Path(__file__).resolve().parent

# Set up the vector store path
VECTOR_STORE_PATH = os.path.join(BASE_DIR, "./data/vector_store")

# Ensure the vector store directory exists
os.makedirs(VECTOR_STORE_PATH, exist_ok=True)

def main():
    """Run the ChromaDB server."""
    logger.info(f"Starting ChromaDB server with data directory: {VECTOR_STORE_PATH}")

    # Import here to avoid circular imports
    import chromadb

    # Create a persistent client that will serve as our server
    client = chromadb.PersistentClient(path=VECTOR_STORE_PATH)

    # Log that the server is running
    logger.info("ChromaDB server is running. Press Ctrl+C to stop.")

    # Keep the script running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("ChromaDB server stopped by user")

if __name__ == "__main__":
    main()
