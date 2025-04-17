#!/usr/bin/env python
"""
Script to start the LLM Chat Indexer application.

This script checks dependencies, starts the ChromaDB server,
and then starts the Flask application.
"""

import logging
import os
import subprocess
import sys
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

def check_dependencies():
    """Check if all required dependencies are installed."""
    logger.info("Checking dependencies...")

    # Run the check_dependencies.py script
    check_script = os.path.join(BASE_DIR, "scripts", "check_dependencies.py")

    if not os.path.exists(check_script):
        logger.error(f"Dependency check script not found: {check_script}")
        return False

    try:
        subprocess.run([sys.executable, check_script], check=True)
        logger.info("All dependencies are installed and working correctly.")
        return True
    except subprocess.CalledProcessError:
        logger.error("Failed to check dependencies.")
        return False

def start_chroma_server():
    """Start the ChromaDB server."""
    logger.info("Starting ChromaDB server...")

    # Run the run_chroma_server.py script
    chroma_script = os.path.join(BASE_DIR, "run_chroma_server.py")

    if not os.path.exists(chroma_script):
        logger.error(f"ChromaDB server script not found: {chroma_script}")
        return None

    try:
        # Start the ChromaDB server as a subprocess
        process = subprocess.Popen(
            [sys.executable, chroma_script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Wait a moment for the server to start
        time.sleep(3)

        # Check if the process is still running
        if process.poll() is not None:
            # Process has terminated
            _, stderr = process.communicate()
            logger.error(f"ChromaDB server failed to start: {stderr}")
            return None

        logger.info("ChromaDB server started successfully.")
        return process
    except Exception as e:
        logger.error(f"Failed to start ChromaDB server: {e}")
        return None

def start_flask_app():
    """Start the Flask application."""
    logger.info("Starting Flask application...")

    # Run the run.py script
    flask_script = os.path.join(BASE_DIR, "run.py")

    if not os.path.exists(flask_script):
        logger.error(f"Flask application script not found: {flask_script}")
        return False

    try:
        # Start the Flask application
        subprocess.run([sys.executable, flask_script], check=True)
        logger.info("Flask application exited.")
        return True
    except subprocess.CalledProcessError:
        logger.error("Flask application failed.")
        return False
    except KeyboardInterrupt:
        logger.info("Flask application stopped by user.")
        return True

def main():
    """Start the LLM Chat Indexer application."""
    logger.info("Starting LLM Chat Indexer application...")

    # Check dependencies
    if not check_dependencies():
        logger.error("Dependency check failed. Please install the required dependencies.")
        return False

    # Start the ChromaDB server
    chroma_process = start_chroma_server()
    if chroma_process is None:
        logger.error("Failed to start ChromaDB server. Exiting.")
        return False

    try:
        # Start the Flask application
        start_flask_app()
    finally:
        # Terminate the ChromaDB server
        logger.info("Terminating ChromaDB server...")
        chroma_process.terminate()
        chroma_process.wait()
        logger.info("ChromaDB server terminated.")

    logger.info("LLM Chat Indexer application stopped.")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
