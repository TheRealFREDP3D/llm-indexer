"""
Tests for the summarization module.
"""

import unittest
import os
from unittest.mock import patch, MagicMock
from src.summarization import generate_summary


class TestSummarization(unittest.TestCase):
    """Test cases for the summarization module."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Sample chat data for testing summarization
        self.chat_data = [
            {"role": "user", "content": "Hello, how are you?"},
            {"role": "assistant", "content": "I'm doing well, thank you for asking!"},
            {"role": "user", "content": "Can you tell me about renewable energy?"},
            {"role": "assistant", "content": "Renewable energy comes from sources that naturally replenish, such as sunlight, wind, rain, tides, waves, and geothermal heat. Unlike fossil fuels, these energy sources won't run out and generally don't produce greenhouse gases."}
        ]
    
    @patch('src.summarization.distiller.GeminiClient')
    def test_generate_summary_gist(self, mock_gemini_client):
        """Test generating a gist summary."""
        # Mock the GeminiClient
        mock_instance = MagicMock()
        mock_gemini_client.return_value = mock_instance
        mock_instance.generate_summary.return_value = "A conversation about renewable energy sources."
        
        # Generate a summary
        summary = generate_summary(self.chat_data, "gist")
        
        # Check that the summary is a string
        self.assertIsInstance(summary, str)
        
        # Check that the GeminiClient was called with the right parameters
        mock_instance.generate_summary.assert_called_once()
        args, kwargs = mock_instance.generate_summary.call_args
        self.assertEqual(kwargs.get('summary_type'), "gist")
    
    @patch('src.summarization.distiller.GeminiClient')
    def test_generate_summary_key_points(self, mock_gemini_client):
        """Test generating a key points summary."""
        # Mock the GeminiClient
        mock_instance = MagicMock()
        mock_gemini_client.return_value = mock_instance
        mock_instance.generate_summary.return_value = "- The user asked about renewable energy\n- The assistant explained different renewable energy sources"
        
        # Generate a summary
        summary = generate_summary(self.chat_data, "key_points")
        
        # Check that the summary is a string
        self.assertIsInstance(summary, str)
        
        # Check that the GeminiClient was called with the right parameters
        mock_instance.generate_summary.assert_called_once()
        args, kwargs = mock_instance.generate_summary.call_args
        self.assertEqual(kwargs.get('summary_type'), "key_points")
    
    def test_generate_summary_invalid_type(self):
        """Test generating a summary with an invalid type."""
        # Check that an invalid summary type raises a ValueError
        with self.assertRaises(ValueError):
            generate_summary(self.chat_data, "invalid_type")


if __name__ == "__main__":
    unittest.main()
