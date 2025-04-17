"""
Tests for the parsing module.

This module tests the JSON and Markdown parsers to ensure they correctly
extract messages from different file formats.
"""

import json
import pytest
from src.parsing import JSONParser, MarkdownParser


def test_json_parser_with_string():
    """Test parsing JSON content from a string."""
    # Sample JSON content
    json_data = json.dumps([
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "assistant", "content": "I'm doing well, thank you for asking!"}
    ])

    parser = JSONParser()
    messages = parser.parse(json_data)

    # Check that we got the expected number of messages
    assert len(messages) == 2

    # Check the first message
    assert messages[0]['role'] == 'user'
    assert messages[0]['content'] == 'Hello, how are you?'

    # Check the second message
    assert messages[1]['role'] == 'assistant'
    assert messages[1]['content'] == "I'm doing well, thank you for asking!"


def test_markdown_parser_with_string():
    """Test parsing Markdown content from a string."""
    # Sample Markdown content
    md_content = """
    ## User:
    Hello, how are you?

    ## Assistant:
    I'm doing well, thank you for asking!
    """

    parser = MarkdownParser()
    messages = parser.parse(md_content)

    # Check that we got the expected number of messages
    assert len(messages) == 2

    # Check the first message
    assert messages[0]['role'] == 'user'
    assert messages[0]['content'] == 'Hello, how are you?'

    # Check the second message
    assert messages[1]['role'] == 'assistant'
    assert messages[1]['content'] == "I'm doing well, thank you for asking!"


def test_json_parser_with_file(sample_json_file):
    """Test parsing JSON content from a file."""
    # Read the sample JSON file
    with open(sample_json_file, 'r', encoding='utf-8') as f:
        content = f.read()

    parser = JSONParser()
    messages = parser.parse(content)

    # Check that we got the expected number of messages
    assert len(messages) == 6

    # Check that the messages have the expected structure
    assert all('role' in message for message in messages)
    assert all('content' in message for message in messages)
    assert all(message['role'] in ['user', 'assistant'] for message in messages)

    # Check for specific content about renewable energy
    assert any('renewable energy' in message['content'].lower() for message in messages), \
        "Expected to find content about renewable energy"


def test_markdown_parser_with_file(sample_md_file):
    """Test parsing Markdown content from a file."""
    # Read the sample Markdown file
    with open(sample_md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    parser = MarkdownParser()
    messages = parser.parse(content)

    # Check that we got the expected number of messages
    assert len(messages) == 6

    # Check that the messages have the expected structure
    assert all('role' in message for message in messages)
    assert all('content' in message for message in messages)
    assert all(message['role'] in ['user', 'assistant'] for message in messages)

    # Check for specific content about renewable energy
    assert any('renewable energy' in message['content'].lower() for message in messages), \
        "Expected to find content about renewable energy"


def test_json_parser_error_handling():
    """Test that the JSON parser handles invalid input gracefully."""
    parser = JSONParser()

    # Test with invalid JSON
    invalid_json = "{\"messages\": ["
    with pytest.raises(ValueError):
        parser.parse(invalid_json)

    # Test with valid JSON but wrong structure
    valid_but_wrong = "{\"not_messages\": []}"
    with pytest.raises(ValueError):
        parser.parse(valid_but_wrong)


def test_markdown_parser_error_handling():
    """Test that the Markdown parser handles invalid input gracefully."""
    parser = MarkdownParser()

    # Test with different types of invalid content
    test_cases = [
        ("", "empty content"),
        ("This is just plain text without any markers.", "content without markers")
    ]

    for content, description in test_cases:
        messages = parser.parse(content)
        assert len(messages) == 0, f"Parser should return empty list for {description}"
