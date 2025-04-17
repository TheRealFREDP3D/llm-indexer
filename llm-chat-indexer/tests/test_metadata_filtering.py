"""
Test metadata filtering functionality.
"""

import unittest
from datetime import datetime
from src.utils.text_utils import filter_complex_metadata
from src.indexing import index_chat
import uuid


class TestMetadataFiltering(unittest.TestCase):
    """Test the metadata filtering functionality."""

    def test_filter_complex_metadata(self):
        """Test that complex metadata is properly filtered."""
        # Create a metadata dictionary with various types
        metadata = {
            'string': 'text',
            'integer': 42,
            'float': 3.14,
            'boolean': True,
            'none': None,
            'datetime': datetime.now(),
            'list': [1, 2, 3],
            'dict': {'key': 'value'}
        }

        # Filter the metadata
        filtered = filter_complex_metadata(metadata)

        # Check that simple types are preserved
        self.assertEqual(filtered['string'], 'text')
        self.assertEqual(filtered['integer'], 42)
        self.assertEqual(filtered['float'], 3.14)
        self.assertEqual(filtered['boolean'], True)

        # Check that None is removed
        self.assertNotIn('none', filtered)

        # Check that complex types are converted to strings
        self.assertIsInstance(filtered['datetime'], str)
        self.assertIsInstance(filtered['list'], str)
        self.assertIsInstance(filtered['dict'], str)

    def test_indexing_with_complex_metadata(self):
        """Test that indexing works with complex metadata."""
        # Create a chat with complex metadata
        chat_id = f"test_{uuid.uuid4()}"
        chat_data = [
            {
                'role': 'user',
                'content': 'Hello, how are you?',
                'timestamp': datetime.now(),
                'complex_field': {'key': 'value'},
                'none_field': None
            },
            {
                'role': 'assistant',
                'content': 'I am doing well, thank you!',
                'timestamp': datetime.now(),
                'list_field': [1, 2, 3]
            }
        ]

        # This should not raise an exception
        try:
            index_chat(chat_data, chat_id)
            success = True
        except Exception as e:
            success = False
            print(f"Indexing failed: {str(e)}")

        self.assertTrue(success, "Indexing with complex metadata should succeed")


if __name__ == '__main__':
    unittest.main()
