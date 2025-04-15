"""
Tests for the parsing module.
"""

import json
import unittest

from src.parsing import JSONParser, MarkdownParser


class TestJSONParser(unittest.TestCase):
    """Test cases for the JSONParser class."""
    
    def test_parse_valid_json(self):
        """Test parsing valid JSON chat data."""
        parser = JSONParser()
        
        # Sample JSON chat data
        json_data = json.dumps([
            {"role": "user", "content": "Hello, how are you?"},
            {"role": "assistant", "content": "I'm doing well, thank you for asking!"}
        ])
        
        # Parse the data
        result = parser.parse(json_data)
        
        # Check the result
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["role"], "user")
        self.assertEqual(result[0]["content"], "Hello, how are you?")
        self.assertEqual(result[1]["role"], "assistant")
        self.assertEqual(result[1]["content"], "I'm doing well, thank you for asking!")
    
    def test_parse_invalid_json(self):
        """Test parsing invalid JSON chat data."""
        parser = JSONParser()
        
        # Invalid JSON data
        json_data = "This is not valid JSON"
        
        # Check that parsing raises an exception
        with self.assertRaises(ValueError):
            parser.parse(json_data)


class TestMarkdownParser(unittest.TestCase):
    """Test cases for the MarkdownParser class."""
    
    def test_parse_markdown(self):
        """Test parsing Markdown chat data."""
        parser = MarkdownParser()
        
        # Sample Markdown chat data
        md_data = """
        ## User:
        Hello, how are you?
        
        ## Assistant:
        I'm doing well, thank you for asking!
        """
        
        # Parse the data
        result = parser.parse(md_data)
        
        # Check the result
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["role"], "user")
        self.assertEqual(result[0]["content"], "Hello, how are you?")
        self.assertEqual(result[1]["role"], "assistant")
        self.assertEqual(result[1]["content"], "I'm doing well, thank you for asking!")


if __name__ == "__main__":
    unittest.main()
