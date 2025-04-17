"""
Tests for the configuration module.

This module tests the Configuration class to ensure it correctly loads,
validates, and provides access to configuration values.
"""

import os
import pytest
from unittest.mock import patch, MagicMock

from config.config import Configuration, ConfigurationError


def test_configuration_initialization():
    """Test that the Configuration class initializes correctly."""
    # Create a Configuration instance
    config = Configuration()
    
    # Check that required attributes exist
    assert hasattr(config, 'VECTOR_STORE_PATH')
    assert hasattr(config, 'KG_PATH')
    assert hasattr(config, 'SENTENCE_TRANSFORMER_MODEL')
    assert hasattr(config, 'CHUNK_SIZE')
    assert hasattr(config, 'CHUNK_OVERLAP')
    assert hasattr(config, 'TOP_K_RESULTS')
    assert hasattr(config, 'CHROMA_SETTINGS')


def test_configuration_default_values():
    """Test that the Configuration class provides default values."""
    # Create a Configuration instance with no environment variables
    with patch.dict(os.environ, {}, clear=True):
        config = Configuration()
        
        # Check default values
        assert config.SENTENCE_TRANSFORMER_MODEL == 'all-MiniLM-L6-v2'
        assert config.CHUNK_SIZE == 1000
        assert config.CHUNK_OVERLAP == 200
        assert config.TOP_K_RESULTS == 5
        assert config.CHROMA_SETTINGS['chroma_server_host'] == 'localhost'
        assert config.CHROMA_SETTINGS['chroma_server_http_port'] == '8000'
        assert config.CHROMA_SETTINGS['allow_reset'] is True


def test_configuration_custom_values():
    """Test that the Configuration class uses custom values from environment variables."""
    # Create a Configuration instance with custom environment variables
    env_vars = {
        'SENTENCE_TRANSFORMER_MODEL': 'custom-model',
        'CHUNK_SIZE': '500',
        'CHUNK_OVERLAP': '100',
        'TOP_K_RESULTS': '10',
        'CHROMA_SERVER_HOST': 'custom-host',
        'CHROMA_SERVER_HTTP_PORT': '9000',
        'ALLOW_RESET': 'False'
    }
    
    with patch.dict(os.environ, env_vars):
        config = Configuration()
        
        # Check custom values
        assert config.SENTENCE_TRANSFORMER_MODEL == 'custom-model'
        assert config.CHUNK_SIZE == 500
        assert config.CHUNK_OVERLAP == 100
        assert config.TOP_K_RESULTS == 10
        assert config.CHROMA_SETTINGS['chroma_server_host'] == 'custom-host'
        assert config.CHROMA_SETTINGS['chroma_server_http_port'] == '9000'
        assert config.CHROMA_SETTINGS['allow_reset'] is False


def test_configuration_path_resolution():
    """Test that the Configuration class resolves relative paths correctly."""
    # Create a Configuration instance with relative paths
    env_vars = {
        'VECTOR_STORE_PATH': './relative/path/to/vector_store',
        'KG_PATH': './relative/path/to/kg'
    }
    
    with patch.dict(os.environ, env_vars):
        config = Configuration()
        
        # Check that paths are absolute
        assert os.path.isabs(config.VECTOR_STORE_PATH)
        assert os.path.isabs(config.KG_PATH)
        
        # Check that paths contain the relative components
        assert 'relative/path/to/vector_store' in config.VECTOR_STORE_PATH
        assert 'relative/path/to/kg' in config.KG_PATH


def test_configuration_directory_creation():
    """Test that the Configuration class creates directories if they don't exist."""
    # Mock os.makedirs to check if it's called
    with patch('os.makedirs') as mock_makedirs:
        config = Configuration()
        
        # Check that makedirs was called for each path
        assert mock_makedirs.call_count >= 2
        mock_makedirs.assert_any_call(config.VECTOR_STORE_PATH, exist_ok=True)
        mock_makedirs.assert_any_call(config.KG_PATH, exist_ok=True)


def test_configuration_get_method():
    """Test the get method of the Configuration class."""
    config = Configuration()
    
    # Test getting existing keys
    assert config.get('SENTENCE_TRANSFORMER_MODEL') == config.SENTENCE_TRANSFORMER_MODEL
    assert config.get('CHUNK_SIZE') == config.CHUNK_SIZE
    
    # Test getting non-existent keys with default
    assert config.get('NON_EXISTENT_KEY', 'default') == 'default'
    
    # Test getting non-existent keys without default
    assert config.get('NON_EXISTENT_KEY') is None


def test_configuration_attribute_access():
    """Test attribute access for the Configuration class."""
    config = Configuration()
    
    # Test accessing existing attributes
    assert config.SENTENCE_TRANSFORMER_MODEL is not None
    assert config.CHUNK_SIZE is not None
    
    # Test accessing non-existent attributes
    with pytest.raises(AttributeError):
        _ = config.NON_EXISTENT_ATTRIBUTE


def test_configuration_item_access():
    """Test dictionary-like access for the Configuration class."""
    config = Configuration()
    
    # Test accessing existing keys
    assert config['SENTENCE_TRANSFORMER_MODEL'] is not None
    assert config['CHUNK_SIZE'] is not None
    
    # Test accessing non-existent keys
    with pytest.raises(KeyError):
        _ = config['NON_EXISTENT_KEY']


def test_configuration_contains():
    """Test the __contains__ method of the Configuration class."""
    config = Configuration()
    
    # Test checking for existing keys
    assert 'SENTENCE_TRANSFORMER_MODEL' in config
    assert 'CHUNK_SIZE' in config
    
    # Test checking for non-existent keys
    assert 'NON_EXISTENT_KEY' not in config
