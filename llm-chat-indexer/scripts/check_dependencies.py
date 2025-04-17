#!/usr/bin/env python
"""
Script to check and install required dependencies.

This script checks if all required dependencies are installed and installs
any missing dependencies. It also checks if the required spaCy model is installed.
"""

import logging
import os
import subprocess
import sys
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Get the base directory
BASE_DIR = Path(__file__).resolve().parent.parent

def check_requirements():
    """Check if all required packages are installed."""
    logger.info("Checking required packages...")
    
    # Get the requirements file path
    requirements_file = os.path.join(BASE_DIR, "requirements.txt")
    
    # Check if the requirements file exists
    if not os.path.exists(requirements_file):
        logger.error(f"Requirements file not found: {requirements_file}")
        return False
    
    # Install the requirements
    try:
        logger.info("Installing required packages...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", requirements_file], check=True)
        logger.info("Required packages installed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install required packages: {e}")
        return False
    
    return True

def check_spacy_model():
    """Check if the required spaCy model is installed."""
    logger.info("Checking spaCy model...")
    
    # Check if spaCy is installed
    try:
        import spacy
        logger.info(f"spaCy version: {spacy.__version__}")
    except ImportError:
        logger.error("spaCy is not installed.")
        return False
    
    # Check if the model is installed
    model_name = "en_core_web_sm"
    try:
        spacy.load(model_name)
        logger.info(f"spaCy model '{model_name}' is installed.")
    except OSError:
        logger.warning(f"spaCy model '{model_name}' is not installed. Installing...")
        try:
            subprocess.run([sys.executable, "-m", "spacy", "download", model_name], check=True)
            logger.info(f"spaCy model '{model_name}' installed successfully.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install spaCy model '{model_name}': {e}")
            return False
    
    return True

def check_chromadb():
    """Check if ChromaDB is installed and working."""
    logger.info("Checking ChromaDB...")
    
    # Check if ChromaDB is installed
    try:
        import chromadb
        logger.info(f"ChromaDB version: {chromadb.__version__}")
    except ImportError:
        logger.error("ChromaDB is not installed.")
        return False
    
    # Try to create a client to check if ChromaDB is working
    try:
        # Create a temporary directory for testing
        import tempfile
        with tempfile.TemporaryDirectory() as temp_dir:
            client = chromadb.PersistentClient(path=temp_dir)
            # Try to create a collection
            collection = client.create_collection("test_collection")
            # Add a document to the collection
            collection.add(
                documents=["This is a test document."],
                metadatas=[{"source": "test"}],
                ids=["test_id"]
            )
            # Query the collection
            results = collection.query(
                query_texts=["test"],
                n_results=1
            )
            # Check if the results are as expected
            if results and len(results["documents"]) > 0:
                logger.info("ChromaDB is working correctly.")
                return True
            else:
                logger.error("ChromaDB query returned unexpected results.")
                return False
    except Exception as e:
        logger.error(f"Failed to test ChromaDB: {e}")
        return False

def main():
    """Check and install required dependencies."""
    logger.info("Checking dependencies...")
    
    # Check requirements
    if not check_requirements():
        logger.error("Failed to install required packages.")
        return False
    
    # Check spaCy model
    if not check_spacy_model():
        logger.error("Failed to install spaCy model.")
        return False
    
    # Check ChromaDB
    if not check_chromadb():
        logger.error("ChromaDB is not working correctly.")
        return False
    
    logger.info("All dependencies are installed and working correctly.")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
