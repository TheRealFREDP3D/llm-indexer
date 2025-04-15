"""
Tests for the utils module.
"""

import unittest

from src.utils.text_utils import clean_text, chunk_text, chunk_messages


class TestTextUtils(unittest.TestCase):
    """Test cases for the text_utils module."""
    
    def test_clean_text(self):
        """Test cleaning text."""
        # Test removing extra whitespace
        text = "This   has    extra   spaces."
        cleaned = clean_text(text)
        self.assertEqual(cleaned, "This has extra spaces.")
        
        # Test removing extra newlines
        text = "Line 1\n\n\n\nLine 2"
        cleaned = clean_text(text)
        self.assertEqual(cleaned, "Line 1\n\nLine 2")
        
        # Test stripping leading/trailing whitespace
        text = "  \n  Text with whitespace  \n  "
        cleaned = clean_text(text)
        self.assertEqual(cleaned, "Text with whitespace")
    
    def test_chunk_text(self):
        """Test chunking text."""
        # Test with text shorter than chunk size
        text = "This is a short text."
        chunks = chunk_text(text, chunk_size=100, chunk_overlap=20)
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0], text)
        
        # Test with text longer than chunk size
        text = "This is the first sentence. This is the second sentence. This is the third sentence."
        chunks = chunk_text(text, chunk_size=30, chunk_overlap=5)
        self.assertTrue(len(chunks) > 1)
        
        # Check that all text is included
        combined = ""
        for i, chunk in enumerate(chunks):
            if i == 0:
                combined += chunk
            else:
                # Account for overlap
                overlap_start = len(combined) - 5
                if overlap_start > 0 and combined[overlap_start:] == chunk[:5]:
                    combined += chunk[5:]
                else:
                    combined += chunk
        
        self.assertEqual(clean_text(text), clean_text(combined))
    
    def test_chunk_messages(self):
        """Test chunking messages."""
        # Test with a list of messages
        messages = [
            {"role": "user", "content": "Hello, how are you?"},
            {"role": "assistant", "content": "I'm doing well, thank you for asking!"}
        ]
        
        chunks = chunk_messages(messages, chunk_size=100, chunk_overlap=20)
        
        # Check that we have the right number of chunks
        self.assertEqual(len(chunks), 2)
        
        # Check that each chunk has the correct metadata
        self.assertEqual(chunks[0][1]["role"], "user")
        self.assertEqual(chunks[0][1]["message_index"], 0)
        self.assertEqual(chunks[1][1]["role"], "assistant")
        self.assertEqual(chunks[1][1]["message_index"], 1)


if __name__ == "__main__":
    unittest.main()
