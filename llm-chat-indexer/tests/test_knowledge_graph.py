"""
Tests for the knowledge graph module.
"""

import unittest
import uuid
import os
import shutil
import networkx as nx
from src.knowledge_graph import build_graph, save_graph, load_graph, export_graph_for_vis
from config.settings import KG_PATH


class TestKnowledgeGraph(unittest.TestCase):
    """Test cases for the knowledge graph module."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a unique test directory for knowledge graphs
        self.test_id = str(uuid.uuid4())
        self.test_kg_path = os.path.join(KG_PATH, f"test_{self.test_id}")
        os.makedirs(self.test_kg_path, exist_ok=True)
        
        # Sample chat data with entities for testing knowledge graph
        self.chat_data = [
            {"role": "user", "content": "Hello, my name is John Smith and I work at Microsoft."},
            {"role": "assistant", "content": "Nice to meet you, John! Microsoft is a great company based in Redmond, Washington."},
            {"role": "user", "content": "I'm working on a project about renewable energy with my colleague Sarah Johnson."},
            {"role": "assistant", "content": "That sounds interesting! Renewable energy is an important topic. I'd be happy to help you and Sarah with your project."}
        ]
        
        # Generate a unique chat ID for testing
        self.chat_id = f"test_chat_{self.test_id}"
    
    def tearDown(self):
        """Tear down test fixtures."""
        # Clean up the test directory
        if os.path.exists(self.test_kg_path):
            shutil.rmtree(self.test_kg_path)
    
    def test_build_graph(self):
        """Test building a knowledge graph."""
        # Build the graph
        graph = build_graph(self.chat_data, self.chat_id)
        
        # Check that the graph is a NetworkX graph
        self.assertIsInstance(graph, nx.Graph)
        
        # Check that the graph has nodes and edges
        self.assertTrue(len(graph.nodes) > 0)
        
        # Check that the graph has the chat_id attribute
        self.assertEqual(graph.graph['chat_id'], self.chat_id)
    
    def test_save_and_load_graph(self):
        """Test saving and loading a knowledge graph."""
        # Build and save the graph
        graph = build_graph(self.chat_data, self.chat_id)
        save_path = save_graph(self.chat_id)
        
        # Check that the file exists
        self.assertTrue(os.path.exists(save_path))
        
        # Load the graph
        loaded_graph = load_graph(self.chat_id)
        
        # Check that the loaded graph is a NetworkX graph
        self.assertIsInstance(loaded_graph, nx.Graph)
        
        # Check that the loaded graph has the same number of nodes and edges
        self.assertEqual(len(graph.nodes), len(loaded_graph.nodes))
        self.assertEqual(len(graph.edges), len(loaded_graph.edges))
        
        # Check that the loaded graph has the chat_id attribute
        self.assertEqual(loaded_graph.graph['chat_id'], self.chat_id)
    
    def test_export_graph_for_vis(self):
        """Test exporting a graph for visualization."""
        # Build and save the graph
        build_graph(self.chat_data, self.chat_id)
        save_graph(self.chat_id)
        
        # Export the graph in JSON format
        json_data = export_graph_for_vis(self.chat_id, format="json")
        
        # Check that the export contains nodes and links
        self.assertIn('nodes', json_data)
        self.assertIn('links', json_data)
        self.assertTrue(len(json_data['nodes']) > 0)
        
        # Export the graph in Cytoscape format
        cytoscape_data = export_graph_for_vis(self.chat_id, format="cytoscape")
        
        # Check that the export contains elements
        self.assertIn('elements', cytoscape_data)
        self.assertTrue(len(cytoscape_data['elements']) > 0)


if __name__ == "__main__":
    unittest.main()
