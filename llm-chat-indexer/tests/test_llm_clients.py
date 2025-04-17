"""
Tests for the LLM clients module.

This module tests the Gemini client to ensure it correctly interacts with
the Google Gemini API for text generation, summarization, and entity extraction.
"""

import pytest
from unittest.mock import patch, MagicMock

from src.llm_clients.gemini_client import GeminiClient


@patch('src.llm_clients.gemini_client.genai')
def test_gemini_client_initialization(mock_genai):
    """Test that the GeminiClient initializes correctly."""
    # Arrange
    api_key = "test_api_key"
    model_name = "test-model"
    
    # Act
    client = GeminiClient(api_key=api_key, model_name=model_name)
    
    # Assert
    mock_genai.configure.assert_called_once_with(api_key=api_key)
    assert client.model_name == model_name


@patch('src.llm_clients.gemini_client.genai')
def test_generate_text(mock_genai):
    """Test that generate_text calls the Gemini API correctly."""
    # Arrange
    mock_model = MagicMock()
    mock_genai.GenerativeModel.return_value = mock_model
    mock_response = MagicMock()
    mock_response.text = "Generated text response"
    mock_model.generate_content.return_value = mock_response
    
    client = GeminiClient(api_key="test_api_key")
    prompt = "Test prompt"
    
    # Act
    result = client.generate_text(prompt)
    
    # Assert
    mock_genai.GenerativeModel.assert_called_once_with("gemini-pro")
    mock_model.generate_content.assert_called_once()
    assert result == "Generated text response"


@patch('src.llm_clients.gemini_client.genai')
def test_generate_text_with_parameters(mock_genai):
    """Test that generate_text passes parameters correctly."""
    # Arrange
    mock_model = MagicMock()
    mock_genai.GenerativeModel.return_value = mock_model
    mock_response = MagicMock()
    mock_response.text = "Generated text response"
    mock_model.generate_content.return_value = mock_response
    
    client = GeminiClient(api_key="test_api_key")
    prompt = "Test prompt"
    temperature = 0.3
    max_tokens = 100
    
    # Act
    result = client.generate_text(prompt, temperature=temperature, max_tokens=max_tokens)
    
    # Assert
    mock_model.generate_content.assert_called_once()
    # Check that the generation config was set with the correct parameters
    call_args = mock_model.generate_content.call_args[1]
    assert 'generation_config' in call_args
    assert call_args['generation_config'].temperature == temperature
    if max_tokens:
        assert call_args['generation_config'].max_output_tokens == max_tokens


@patch('src.llm_clients.gemini_client.genai')
def test_generate_text_error_handling(mock_genai):
    """Test that generate_text handles errors correctly."""
    # Arrange
    mock_model = MagicMock()
    mock_genai.GenerativeModel.return_value = mock_model
    mock_model.generate_content.side_effect = Exception("API error")
    
    client = GeminiClient(api_key="test_api_key")
    prompt = "Test prompt"
    
    # Act & Assert
    with pytest.raises(RuntimeError) as excinfo:
        client.generate_text(prompt)
    
    assert "Error generating text with Gemini" in str(excinfo.value)


@patch('src.llm_clients.gemini_client.GeminiClient.generate_text')
def test_generate_summary(mock_generate_text):
    """Test that generate_summary calls generate_text with the correct prompt."""
    # Arrange
    mock_generate_text.return_value = "Summary of the conversation"
    client = GeminiClient(api_key="test_api_key")
    
    messages = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there"}
    ]
    
    # Act
    result = client.generate_summary(messages, summary_type="gist")
    
    # Assert
    mock_generate_text.assert_called_once()
    call_args = mock_generate_text.call_args[0][0]  # Get the prompt
    assert "gist" in call_args.lower()
    assert result == "Summary of the conversation"


@patch('src.llm_clients.gemini_client.GeminiClient.generate_text')
def test_extract_entities(mock_generate_text):
    """Test that extract_entities calls generate_text with the correct prompt."""
    # Arrange
    mock_generate_text.return_value = '[{"entity": "John", "type": "person"}]'
    client = GeminiClient(api_key="test_api_key")
    text = "John works at Microsoft."
    
    # Act
    result = client.extract_entities(text)
    
    # Assert
    mock_generate_text.assert_called_once()
    call_args = mock_generate_text.call_args[0][0]  # Get the prompt
    assert "Extract the key entities" in call_args
    assert text in call_args
    assert result == '[{"entity": "John", "type": "person"}]'
