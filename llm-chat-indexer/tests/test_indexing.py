"""
Tests for the indexing module.
"""

import unittest
import uuid
import os
import shutil
from src.indexing import index_chat, get_collection_names
from src.parsing import JSONParser
from config.settings import VECTOR_STORE_PATH


class TestIndexing(unittest.TestCase):
    """Test cases for the indexing module."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a unique test directory for vector store
        self.test_id = str(uuid.uuid4())
        self.test_vector_store_path = os.path.join(VECTOR_STORE_PATH, f"test_{self.test_id}")
        os.makedirs(self.test_vector_store_path, exist_ok=True)
        
        # Sample chat data
        self.chat_data = [
            {"role": "user", "content": "Hello, how are you?"},
            {"role": "assistant", "content": "I'm doing well, thank you for asking!"},
            {"role": "user", "content": "Can you tell me about renewable energy?"},
            {"role": "assistant", "content": "Renewable energy comes from sources that naturally replenish, such as sunlight, wind, rain, tides, waves, and geothermal heat. Unlike fossil fuels, these energy sources won't run out and generally don't produce greenhouse gases."}
        ]
        
        # Generate a unique chat ID for testing
        self.chat_id = f"test_chat_{self.test_id}"
    
    def tearDown(self):
        """Tear down test fixtures."""
        # Clean up the test directory
        if os.path.exists(self.test_vector_store_path):
            shutil.rmtree(self.test_vector_store_path)
    
    def test_index_chat(self):
        """Test indexing a chat."""
        # Index the chat
        result_id = index_chat(self.chat_data, self.chat_id)
        
        # Check that the returned ID matches the input ID
        self.assertEqual(result_id, self.chat_id)
        
        # Check that the collection was created
        collections = get_collection_names()
        expected_collection = f"chat_{self.chat_id}"
        self.assertIn(expected_collection, collections)
    
    def test_get_collection_names(self):
        """Test getting collection names."""
        # Index a chat to create a collection
        index_chat(self.chat_data, self.chat_id)
        
        # Get collection names
        collections = get_collection_names()
        
        # Check that the collection exists
        expected_collection = f"chat_{self.chat_id}"
        self.assertIn(expected_collection, collections)


if __name__ == "__main__":
    unittest.main()
