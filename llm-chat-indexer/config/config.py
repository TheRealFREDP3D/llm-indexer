"""
Configuration management for the LLM Chat Indexer.

This module provides a Configuration class that handles loading, validating,
and accessing configuration values from environment variables and default settings.
It ensures that required values are present and that optional values have
appropriate defaults.
"""

import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional

from dotenv import load_dotenv

# Set up logging
logger = logging.getLogger(__name__)


class ConfigurationError(Exception):
    """Exception raised for configuration errors."""
    pass


class Configuration:
    """
    Configuration manager for the LLM Chat Indexer.

    This class handles loading configuration values from environment variables,
    validating required values, and providing default values for optional settings.
    It also ensures that paths are properly resolved relative to the base directory.
    """

    # Define required environment variables
    REQUIRED_VARS = [
        # No strictly required variables, but we'll warn if API keys are missing
    ]

    # Define optional environment variables with default values
    OPTIONAL_VARS = {
        'VECTOR_STORE_PATH': './data/vector_store',
        'KG_PATH': './data/knowledge_graphs',
        'SENTENCE_TRANSFORMER_MODEL': 'all-MiniLM-L6-v2',
        'TOP_K_RESULTS': '5',
        'CHUNK_SIZE': '1000',
        'CHUNK_OVERLAP': '200',
        'CHROMA_SERVER_HOST': 'localhost',
        'CHROMA_SERVER_HTTP_PORT': '8000',
        'ALLOW_RESET': 'True',
    }

    # Define API keys that should be present but might be optional in some contexts
    API_KEYS = [
        'GEMINI_API_KEY',
    ]

    def __init__(self, env_file: Optional[str] = None, base_dir: Optional[Path] = None):
        """
        Initialize the configuration manager.

        Args:
            env_file (Optional[str]): Path to the .env file to load.
                If None, the default .env file in the project root is used.
            base_dir (Optional[Path]): Base directory for resolving relative paths.
                If None, the directory containing this file is used.
        """
        # Load environment variables
        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv()

        # Set base directory
        if base_dir:
            self.base_dir = base_dir
        else:
            self.base_dir = Path(__file__).resolve().parent.parent

        # Load and validate configuration
        self._config = self._load_config()
        self._validate_config()

        # Ensure data directories exist
        self._ensure_directories()

    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration values from environment variables.

        Returns:
            Dict[str, Any]: Dictionary of configuration values.
        """
        config = {}

        # Load required variables
        for var in self.REQUIRED_VARS:
            value = os.getenv(var)
            config[var] = value

        # Load optional variables with defaults
        for var, default in self.OPTIONAL_VARS.items():
            value = os.getenv(var, default)

            # Convert numeric values
            if var in ['TOP_K_RESULTS', 'CHUNK_SIZE', 'CHUNK_OVERLAP']:
                try:
                    value = int(value)
                except ValueError:
                    logger.warning(f"Invalid value for {var}: {value}. Using default: {default}")
                    value = int(default)

            # Convert boolean values
            elif var in ['ALLOW_RESET']:
                value = value.lower() in ['true', 'yes', '1', 't', 'y']

            config[var] = value

        # Load API keys
        for key in self.API_KEYS:
            value = os.getenv(key)
            if not value:
                logger.warning(f"API key {key} is not set. Some functionality may be limited.")
            config[key] = value

        # Resolve paths
        for path_var in ['VECTOR_STORE_PATH', 'KG_PATH']:
            if path_var in config and config[path_var]:
                path = config[path_var]
                if not os.path.isabs(path):
                    config[path_var] = os.path.join(self.base_dir, path)

        # Set up ChromaDB settings
        # We support both embedded mode and server mode
        # For embedded mode (default):
        config['CHROMA_SETTINGS'] = {
            "chroma_db_impl": "duckdb+parquet",
            "persist_directory": config['VECTOR_STORE_PATH'],
            "allow_reset": config['ALLOW_RESET']
        }

        # For server mode (when running ChromaDB as a separate server):
        config['CHROMA_SERVER_SETTINGS'] = {
            "chroma_api_impl": "rest",
            "chroma_server_host": config['CHROMA_SERVER_HOST'],
            "chroma_server_http_port": config['CHROMA_SERVER_HTTP_PORT'],
            "allow_reset": config['ALLOW_RESET']
        }

        return config

    def _validate_config(self) -> None:
        """
        Validate the configuration values.

        Raises:
            ConfigurationError: If any required values are missing or invalid.
        """
        # Check required variables
        missing_vars = []
        for var in self.REQUIRED_VARS:
            if not self._config.get(var):
                missing_vars.append(var)

        if missing_vars:
            raise ConfigurationError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )

        # Validate paths
        for path_var in ['VECTOR_STORE_PATH', 'KG_PATH']:
            path = self._config.get(path_var)
            if path and not os.access(os.path.dirname(path), os.W_OK):
                logger.warning(
                    f"Path {path} may not be writable. "
                    f"Please check permissions for {path_var}."
                )

    def _ensure_directories(self) -> None:
        """Ensure that required directories exist."""
        for path_var in ['VECTOR_STORE_PATH', 'KG_PATH']:
            path = self._config.get(path_var)
            if path:
                os.makedirs(path, exist_ok=True)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.

        Args:
            key (str): The configuration key to get.
            default (Any, optional): Default value if the key is not found.

        Returns:
            Any: The configuration value, or the default if not found.
        """
        return self._config.get(key, default)

    def __getattr__(self, name: str) -> Any:
        """
        Get a configuration value as an attribute.

        Args:
            name (str): The attribute name (configuration key).

        Returns:
            Any: The configuration value.

        Raises:
            AttributeError: If the configuration key is not found.
        """
        if name in self._config:
            return self._config[name]
        raise AttributeError(f"Configuration has no attribute '{name}'")

    def __getitem__(self, key: str) -> Any:
        """
        Get a configuration value using dictionary-like access.

        Args:
            key (str): The configuration key to get.

        Returns:
            Any: The configuration value.

        Raises:
            KeyError: If the configuration key is not found.
        """
        if key in self._config:
            return self._config[key]
        raise KeyError(key)

    def __contains__(self, key: str) -> bool:
        """
        Check if a configuration key exists.

        Args:
            key (str): The configuration key to check.

        Returns:
            bool: True if the key exists, False otherwise.
        """
        return key in self._config


# Create a singleton instance
config = Configuration()
