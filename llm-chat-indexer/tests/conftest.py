"""
Test fixtures for the LLM Chat Indexer.

This module provides pytest fixtures that can be used across all test files.
It includes fixtures for sample data, temporary directories, and mock objects.
"""

import os
import json
import uuid
import shutil
import pytest
from unittest.mock import MagicMock

from config.settings import VECTOR_STORE_PATH, KG_PATH


@pytest.fixture
def sample_chat_data():
    """
    Fixture providing sample chat data for testing.
    
    Returns:
        list: A list of message dictionaries with role, content, and timestamp.
    """
    return [
        {"role": "user", "content": "Hello, how are you?", "timestamp": "2023-01-01T12:00:00Z"},
        {"role": "assistant", "content": "I'm doing well, thank you for asking!", "timestamp": "2023-01-01T12:00:05Z"},
        {"role": "user", "content": "Can you tell me about renewable energy?", "timestamp": "2023-01-01T12:00:30Z"},
        {"role": "assistant", "content": "Renewable energy comes from sources that naturally replenish, such as sunlight, wind, rain, tides, waves, and geothermal heat. Unlike fossil fuels, these energy sources won't run out and generally don't produce greenhouse gases.", "timestamp": "2023-01-01T12:00:45Z"}
    ]


@pytest.fixture
def entities_chat_data():
    """
    Fixture providing chat data with named entities for testing knowledge graphs.
    
    Returns:
        list: A list of message dictionaries containing named entities.
    """
    return [
        {"role": "user", "content": "Hello, my name is John Smith and I work at Microsoft.", "timestamp": "2023-01-01T12:00:00Z"},
        {"role": "assistant", "content": "Nice to meet you, John! Microsoft is a great company based in Redmond, Washington.", "timestamp": "2023-01-01T12:00:05Z"},
        {"role": "user", "content": "I'm working on a project about renewable energy with my colleague Sarah Johnson.", "timestamp": "2023-01-01T12:00:30Z"},
        {"role": "assistant", "content": "That sounds interesting! Renewable energy is an important topic. I'd be happy to help you and Sarah with your project.", "timestamp": "2023-01-01T12:00:45Z"}
    ]


@pytest.fixture
def test_chat_id():
    """
    Fixture providing a unique chat ID for testing.
    
    Returns:
        str: A unique chat ID string.
    """
    return f"test_chat_{uuid.uuid4()}"


@pytest.fixture
def test_vector_store_path():
    """
    Fixture providing a temporary vector store path for testing.
    
    This fixture creates a temporary directory for the vector store and
    cleans it up after the test is complete.
    
    Returns:
        str: Path to the temporary vector store directory.
    """
    # Create a unique test directory
    test_id = str(uuid.uuid4())
    test_path = os.path.join(VECTOR_STORE_PATH, f"test_{test_id}")
    os.makedirs(test_path, exist_ok=True)
    
    # Return the path for use in tests
    yield test_path
    
    # Clean up after the test
    if os.path.exists(test_path):
        shutil.rmtree(test_path)


@pytest.fixture
def test_kg_path():
    """
    Fixture providing a temporary knowledge graph path for testing.
    
    This fixture creates a temporary directory for knowledge graphs and
    cleans it up after the test is complete.
    
    Returns:
        str: Path to the temporary knowledge graph directory.
    """
    # Create a unique test directory
    test_id = str(uuid.uuid4())
    test_path = os.path.join(KG_PATH, f"test_{test_id}")
    os.makedirs(test_path, exist_ok=True)
    
    # Return the path for use in tests
    yield test_path
    
    # Clean up after the test
    if os.path.exists(test_path):
        shutil.rmtree(test_path)


@pytest.fixture
def mock_gemini_client():
    """
    Fixture providing a mock GeminiClient for testing.
    
    Returns:
        MagicMock: A mock GeminiClient object.
    """
    mock_client = MagicMock()
    mock_client.generate_text.return_value = "This is a mock response from Gemini."
    mock_client.generate_summary.return_value = "This is a mock summary from Gemini."
    mock_client.extract_entities.return_value = '[{"entity": "John Smith", "type": "person"}, {"entity": "Microsoft", "type": "organization"}]'
    return mock_client


@pytest.fixture
def sample_json_file():
    """
    Fixture providing the path to a sample JSON chat file.
    
    Returns:
        str: Path to the sample JSON file.
    """
    return os.path.join('tests', 'fixtures', 'sample_chat.json')


@pytest.fixture
def sample_md_file():
    """
    Fixture providing the path to a sample Markdown chat file.
    
    Returns:
        str: Path to the sample Markdown file.
    """
    return os.path.join('tests', 'fixtures', 'sample_chat.md')


@pytest.fixture
def entities_json_file():
    """
    Fixture providing the path to a JSON chat file with named entities.
    
    Returns:
        str: Path to the entities JSON file.
    """
    return os.path.join('tests', 'fixtures', 'entities_chat.json')
