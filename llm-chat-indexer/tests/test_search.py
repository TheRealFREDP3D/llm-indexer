"""
Tests for the search module.
"""

import unittest
import uuid
import os
import shutil
from src.indexing import index_chat
from src.search import search, search_all_collections
from config.settings import VECTOR_STORE_PATH


class TestSearch(unittest.TestCase):
    """Test cases for the search module."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a unique test directory for vector store
        self.test_id = str(uuid.uuid4())
        self.test_vector_store_path = os.path.join(VECTOR_STORE_PATH, f"test_{self.test_id}")
        os.makedirs(self.test_vector_store_path, exist_ok=True)
        
        # Sample chat data with specific content for testing search
        self.chat_data = [
            {"role": "user", "content": "Hello, how are you?"},
            {"role": "assistant", "content": "I'm doing well, thank you for asking!"},
            {"role": "user", "content": "Can you tell me about renewable energy?"},
            {"role": "assistant", "content": "Renewable energy comes from sources that naturally replenish, such as sunlight, wind, rain, tides, waves, and geothermal heat. Unlike fossil fuels, these energy sources won't run out and generally don't produce greenhouse gases."}
        ]
        
        # Generate a unique chat ID for testing
        self.chat_id = f"test_chat_{self.test_id}"
        
        # Index the chat for searching
        index_chat(self.chat_data, self.chat_id)
    
    def tearDown(self):
        """Tear down test fixtures."""
        # Clean up the test directory
        if os.path.exists(self.test_vector_store_path):
            shutil.rmtree(self.test_vector_store_path)
    
    def test_search(self):
        """Test searching in a specific chat."""
        # Search for a term that should be in the chat
        query = "renewable energy"
        results = search(query, self.chat_id)
        
        # Check that we got results
        self.assertTrue(len(results) > 0)
        
        # Check that the results contain the expected content
        found_match = False
        for result in results:
            if "renewable energy" in result['text'].lower():
                found_match = True
                break
        
        self.assertTrue(found_match, "Search results should contain the query term")
    
    def test_search_all_collections(self):
        """Test searching across all collections."""
        # Search for a term that should be in the chat
        query = "renewable energy"
        results = search_all_collections(query)
        
        # Check that we got results
        self.assertTrue(len(results) > 0)
        
        # Check that the results contain our test chat
        self.assertIn(self.chat_id, results)
        
        # Check that the results contain the expected content
        found_match = False
        for result in results[self.chat_id]:
            if "renewable energy" in result['text'].lower():
                found_match = True
                break
        
        self.assertTrue(found_match, "Search results should contain the query term")


if __name__ == "__main__":
    unittest.main()
