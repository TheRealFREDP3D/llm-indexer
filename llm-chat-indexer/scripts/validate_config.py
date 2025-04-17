#!/usr/bin/env python
"""
Configuration validation script for LLM Chat Indexer.

This script validates the configuration settings for the LLM Chat Indexer
and reports any issues or warnings. It's useful for checking that the
environment is properly set up before running the application.
"""

import os
import sys
import logging
from pathlib import Path

# Add the parent directory to the path so we can import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.config import Configuration, ConfigurationError

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


def validate_config(env_file=None):
    """
    Validate the configuration settings.
    
    Args:
        env_file (str, optional): Path to the .env file to load.
    
    Returns:
        bool: True if the configuration is valid, False otherwise.
    """
    try:
        # Load the configuration
        config = Configuration(env_file=env_file)
        
        # Check API keys
        missing_keys = []
        if not config.GEMINI_API_KEY:
            missing_keys.append('GEMINI_API_KEY')
        
        if missing_keys:
            logger.warning(
                f"The following API keys are missing: {', '.join(missing_keys)}. "
                f"Some functionality may be limited."
            )
        
        # Check paths
        for path_var in ['VECTOR_STORE_PATH', 'KG_PATH']:
            path = getattr(config, path_var)
            if not os.path.exists(path):
                logger.warning(f"{path_var} directory does not exist: {path}")
            elif not os.access(path, os.W_OK):
                logger.warning(f"{path_var} directory is not writable: {path}")
        
        # Check model settings
        if not config.SENTENCE_TRANSFORMER_MODEL:
            logger.warning("SENTENCE_TRANSFORMER_MODEL is not set. Using default model.")
        
        # Check ChromaDB settings
        if config.CHROMA_SETTINGS['allow_reset'] and 'production' in os.getenv('ENV', '').lower():
            logger.warning(
                "ALLOW_RESET is set to True in a production environment. "
                "This may be a security risk."
            )
        
        logger.info("Configuration validation completed successfully.")
        return True
        
    except ConfigurationError as e:
        logger.error(f"Configuration error: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during configuration validation: {str(e)}")
        return False


def main():
    """Main entry point for the script."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Validate LLM Chat Indexer configuration.')
    parser.add_argument('--env-file', type=str, help='Path to the .env file to load')
    args = parser.parse_args()
    
    success = validate_config(env_file=args.env_file)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
