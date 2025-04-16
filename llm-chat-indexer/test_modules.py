"""
Test script to verify that the core modules are working correctly.
"""

import os
import json
from src.parsing import JSONParser, MarkdownParser
from src.utils.text_utils import clean_text, chunk_text, chunk_messages
from src.indexing import index_chat, get_collection_names
from src.search import search, search_all_collections
from src.knowledge_graph import build_graph, save_graph, export_graph_for_vis

def test_parsing():
    """Test the parsing modules."""
    print("Testing parsing modules...")
    
    # Test JSON parser
    json_file = os.path.join('data', 'raw_chats', 'sample_chat.json')
    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        json_parser = JSONParser()
        messages = json_parser.parse(content)
        print(f"JSON Parser: Successfully parsed {len(messages)} messages")
        print(f"First message: {messages[0]['role']}: {messages[0]['content'][:50]}...")
    else:
        print(f"JSON file not found: {json_file}")
    
    # Test Markdown parser
    md_file = os.path.join('data', 'raw_chats', 'sample_chat.md')
    if os.path.exists(md_file):
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        md_parser = MarkdownParser()
        messages = md_parser.parse(content)
        print(f"Markdown Parser: Successfully parsed {len(messages)} messages")
        print(f"First message: {messages[0]['role']}: {messages[0]['content'][:50]}...")
    else:
        print(f"Markdown file not found: {md_file}")

def test_utils():
    """Test the utility functions."""
    print("\nTesting utility functions...")
    
    # Test clean_text
    text = "This   has    extra   spaces.\n\n\n\nAnd extra newlines."
    cleaned = clean_text(text)
    print(f"Clean text: '{cleaned}'")
    
    # Test chunk_text
    chunks = chunk_text(text, chunk_size=20, chunk_overlap=5)
    print(f"Chunked text into {len(chunks)} chunks")
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}: '{chunk}'")
    
    # Test chunk_messages
    messages = [
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "assistant", "content": "I'm doing well, thank you for asking!"}
    ]
    chunks_with_metadata = chunk_messages(messages, chunk_size=20, chunk_overlap=5)
    print(f"Chunked messages into {len(chunks_with_metadata)} chunks with metadata")
    for i, (chunk, metadata) in enumerate(chunks_with_metadata):
        print(f"Chunk {i+1}: '{chunk}', Role: {metadata['role']}")

def test_indexing_and_search():
    """Test the indexing and search modules."""
    print("\nTesting indexing and search modules...")
    
    # Test indexing
    json_file = os.path.join('data', 'raw_chats', 'sample_chat.json')
    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        json_parser = JSONParser()
        messages = json_parser.parse(content)
        
        # Generate a test chat ID
        chat_id = "test_chat_001"
        
        try:
            # Index the chat
            index_chat(messages, chat_id)
            print(f"Successfully indexed chat with ID: {chat_id}")
            
            # Get collection names
            collections = get_collection_names()
            print(f"Collections: {collections}")
            
            # Test search
            query = "renewable energy"
            results = search(query, chat_id)
            print(f"Search results for '{query}': {len(results)} hits")
            if results:
                print(f"Top result: '{results[0]['text'][:50]}...'")
            
            # Test search all collections
            all_results = search_all_collections(query)
            print(f"Search all collections for '{query}': {len(all_results)} collections with hits")
            
        except Exception as e:
            print(f"Error in indexing or search: {str(e)}")
    else:
        print(f"JSON file not found: {json_file}")

def test_knowledge_graph():
    """Test the knowledge graph module."""
    print("\nTesting knowledge graph module...")
    
    # Test building a knowledge graph
    json_file = os.path.join('data', 'raw_chats', 'sample_chat.json')
    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        json_parser = JSONParser()
        messages = json_parser.parse(content)
        
        # Generate a test chat ID
        chat_id = "test_chat_001"
        
        try:
            # Build the graph
            graph = build_graph(messages, chat_id)
            print(f"Successfully built graph with {len(graph.nodes)} nodes and {len(graph.edges)} edges")
            
            # Save the graph
            graph_path = save_graph(chat_id)
            print(f"Saved graph to: {graph_path}")
            
            # Export the graph for visualization
            graph_data = export_graph_for_vis(chat_id)
            print(f"Exported graph with {len(graph_data['nodes'])} nodes and {len(graph_data['links'])} links")
            
        except Exception as e:
            print(f"Error in knowledge graph: {str(e)}")
    else:
        print(f"JSON file not found: {json_file}")

if __name__ == "__main__":
    test_parsing()
    test_utils()
    test_indexing_and_search()
    test_knowledge_graph()
