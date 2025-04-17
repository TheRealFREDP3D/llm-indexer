"""
Test the LangChain integration for indexing and searching chat data.
"""

import shutil
import uuid
from datetime import datetime
from pathlib import Path

import pytest
from config.settings import VECTOR_STORE_PATH
from src.indexing import get_collection_names, index_chat
from src.search import search, search_all_collections

# Sample chat data for testing
SAMPLE_CHAT = [
    {
        "role": "user",
        "content": "How do I implement a binary search tree in Python?",
        "timestamp": datetime.now().isoformat(),
        "id": "msg1"
    },
    {
        "role": "assistant",
        "content": """Here's how to implement a basic binary search tree in Python:

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None
        
    def insert(self, value):
        if not self.root:
            self.root = Node(value)
        else:
            self._insert_recursive(self.root, value)
            
    def _insert_recursive(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = Node(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = Node(value)
            else:
                self._insert_recursive(node.right, value)
```

This implementation includes the basic structure and insert operation.""",
        "timestamp": datetime.now().isoformat(),
        "id": "msg2"
    },
    {
        "role": "user",
        "content": "How would I add a search method to find a value in the tree?",
        "timestamp": datetime.now().isoformat(),
        "id": "msg3"
    },
    {
        "role": "assistant",
        "content": """You can add a search method like this:

```python
def search(self, value):
    return self._search_recursive(self.root, value)
    
def _search_recursive(self, node, value):
    if node is None or node.value == value:
        return node
    if value < node.value:
        return self._search_recursive(node.left, value)
    return self._search_recursive(node.right, value)
```

This will return the node containing the value if found, or None if not found.""",
        "timestamp": datetime.now().isoformat(),
        "id": "msg4"
    }
]

@pytest.fixture
def clean_vector_store():
    """Fixture to ensure a clean vector store for each test."""
    # Create vector store directory if it doesn't exist
    vector_store_path = Path(VECTOR_STORE_PATH)
    vector_store_path.mkdir(parents=True, exist_ok=True)
    
    # Clean up any existing test collections
    for path in vector_store_path.glob("chat_test_*"):
        if path.is_dir():
            shutil.rmtree(path)
    
    yield
    
    # Clean up after tests
    for path in vector_store_path.glob("chat_test_*"):
        if path.is_dir():
            shutil.rmtree(path)

def test_index_and_search(clean_vector_store):
    """Test indexing and searching chat data."""
    # Generate a unique chat ID for testing
    chat_id = f"test_{uuid.uuid4()}"
    
    # Index the sample chat
    index_chat(SAMPLE_CHAT, chat_id)
    
    # Verify the collection was created
    collections = get_collection_names()
    assert f"chat_{chat_id}" in collections
    
    # Test searching within the chat
    results = search("binary search tree implementation", chat_id)
    assert len(results) > 0
    assert any("binary search tree" in result["text"].lower() for result in results)
    
    # Test searching for Python code
    results = search("search method implementation", chat_id)
    assert len(results) > 0
    assert any("def search" in result["text"] for result in results)
    
    # Test searching across all collections
    all_results = search_all_collections("binary search tree")
    assert chat_id in all_results
    assert len(all_results[chat_id]) > 0

def test_metadata_preservation(clean_vector_store):
    """Test that message metadata is preserved during indexing and searching."""
    chat_id = f"test_{uuid.uuid4()}"
    
    # Index the sample chat
    index_chat(SAMPLE_CHAT, chat_id)
    
    # Search and verify metadata
    results = search("binary search tree", chat_id)
    assert len(results) > 0
    
    for result in results:
        assert "metadata" in result
        assert "role" in result["metadata"]
        assert result["metadata"]["role"] in ["user", "assistant"]
        assert "message_id" in result["metadata"]
        assert "timestamp" in result["metadata"]

def test_multiple_chats(clean_vector_store):
    """Test indexing and searching multiple chats."""
    # Create two different chats
    chat1_id = f"test_{uuid.uuid4()}"
    chat2_id = f"test_{uuid.uuid4()}"
    
    # Modify the second message for chat2
    chat2_data = SAMPLE_CHAT.copy()
    chat2_data[1]["content"] = """Here's a simple implementation of quicksort in Python:

```python
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)
```"""
    
    # Index both chats
    index_chat(SAMPLE_CHAT, chat1_id)
    index_chat(chat2_data, chat2_id)
    
    # Search across all collections
    results = search_all_collections("sorting algorithm")
    assert chat2_id in results  # Should find quicksort
    assert len(results[chat2_id]) > 0
    assert any("quicksort" in result["text"].lower() for result in results[chat2_id])
    
    results = search_all_collections("binary search tree")
    assert chat1_id in results  # Should find BST
    assert len(results[chat1_id]) > 0
    assert any("binary search tree" in result["text"].lower() for result in results[chat1_id])

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 