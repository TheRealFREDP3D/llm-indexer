"""
Integration tests for the LLM Chat Indexer.

This module tests the end-to-end workflow of the application, from parsing
chat data to indexing, searching, and generating knowledge graphs.
"""

import os
import json
import pytest
from unittest.mock import patch

from src.parsing import JSONParser
from src.indexing import index_chat, get_collection_names
from src.search import search, search_all_collections
from src.knowledge_graph import build_graph, save_graph, export_graph_for_vis
from src.summarization import generate_summary


@pytest.mark.integration
def test_full_workflow(sample_json_file, test_chat_id, mock_gemini_client):
    """
    Test the full workflow from parsing to search and knowledge graph generation.
    
    This test simulates the entire process a user would go through:
    1. Parse a chat file
    2. Index the chat
    3. Search within the chat
    4. Generate a knowledge graph
    5. Generate a summary
    
    All external API calls are mocked to ensure the test is self-contained.
    """
    # Step 1: Parse the chat file
    with open(sample_json_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    parser = JSONParser()
    messages = parser.parse(content)
    
    # Verify parsing was successful
    assert len(messages) > 0
    assert all('role' in message for message in messages)
    assert all('content' in message for message in messages)
    
    # Step 2: Index the chat
    chat_id = index_chat(messages, test_chat_id)
    
    # Verify indexing was successful
    assert chat_id == test_chat_id
    collections = get_collection_names()
    assert f"chat_{test_chat_id}" in collections
    
    # Step 3: Search within the chat
    search_results = search("renewable energy", test_chat_id)
    
    # Verify search was successful
    assert len(search_results) > 0
    assert any('renewable energy' in result['text'].lower() for result in search_results)
    
    # Step 4: Search across all collections
    all_results = search_all_collections("renewable energy")
    
    # Verify search across collections was successful
    assert len(all_results) > 0
    assert test_chat_id in all_results
    
    # Step 5: Build a knowledge graph
    with patch('src.knowledge_graph.builder.GeminiClient') as mock_client:
        mock_client.return_value = mock_gemini_client
        graph = build_graph(messages, test_chat_id)
        
        # Verify graph building was successful
        assert graph is not None
        assert len(graph.nodes) > 0
        
        # Save the graph
        graph_path = save_graph(test_chat_id)
        
        # Verify graph saving was successful
        assert os.path.exists(graph_path)
        
        # Export the graph for visualization
        graph_data = export_graph_for_vis(test_chat_id)
        
        # Verify graph export was successful
        assert 'nodes' in graph_data
        assert 'links' in graph_data
    
    # Step 6: Generate a summary
    with patch('src.summarization.distiller.GeminiClient') as mock_client:
        mock_client.return_value = mock_gemini_client
        summary = generate_summary(messages, "gist")
        
        # Verify summary generation was successful
        assert summary is not None
        assert len(summary) > 0


@pytest.mark.integration
def test_workflow_with_empty_chat():
    """
    Test the workflow with an empty chat to ensure graceful handling.
    
    This test verifies that the application handles edge cases properly,
    such as empty chat data or no search results.
    """
    # Create empty messages
    messages = []
    chat_id = "empty_chat_test"
    
    # Index the empty chat (should not raise errors)
    index_chat(messages, chat_id)
    
    # Search should return empty results
    search_results = search("test query", chat_id)
    assert len(search_results) == 0
    
    # Knowledge graph should be minimal
    with patch('src.knowledge_graph.builder.GeminiClient'):
        graph = build_graph(messages, chat_id)
        assert len(graph.nodes) == 0
