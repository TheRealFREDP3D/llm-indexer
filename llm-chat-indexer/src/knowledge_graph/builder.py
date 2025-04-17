"""
Knowledge graph builder for chat data.
"""

import os
import json
import pickle
from typing import List, Dict, Any, Optional, Tuple, Set

import spacy
import networkx as nx

from config.settings import KG_PATH


class KnowledgeGraphBuilder:
    """
    Class for building knowledge graphs from chat data using spaCy and NetworkX.
    """

    def __init__(self, spacy_model: str = "en_core_web_sm"):
        """
        Initialize the knowledge graph builder with a spaCy model.

        Args:
            spacy_model (str): Name of the spaCy model to use.
        """
        self.spacy_model_name = spacy_model

        # Load the spaCy model
        self.nlp = spacy.load(spacy_model)

        # Initialize an empty graph
        self.graph = nx.Graph()

    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract named entities from text using spaCy.

        Args:
            text (str): The text to extract entities from.

        Returns:
            List[Dict[str, Any]]: List of extracted entities with their types.
        """
        doc = self.nlp(text)

        entities = []
        for ent in doc.ents:
            entities.append({
                'text': ent.text,
                'label': ent.label_,
                'start': ent.start_char,
                'end': ent.end_char
            })

        return entities

    def extract_relationships(self, text: str) -> List[Tuple[str, str, str]]:
        """
        Extract relationships between entities using spaCy's dependency parsing.
        This is a simplified approach and may not capture all relationships accurately.

        Args:
            text (str): The text to extract relationships from.

        Returns:
            List[Tuple[str, str, str]]: List of (subject, predicate, object) triples.
        """
        doc = self.nlp(text)

        # Extract subject-verb-object triples
        triples = []

        for token in doc:
            # Look for verbs
            if token.pos_ == "VERB":
                # Find the subject
                subjects = [subj for subj in token.children if subj.dep_ in ("nsubj", "nsubjpass")]

                # Find the object
                objects = [obj for obj in token.children if obj.dep_ in ("dobj", "pobj", "attr")]

                # Create triples for all subject-object combinations
                for subj in subjects:
                    subj_span = self._get_span_with_compounds(subj)

                    for obj in objects:
                        obj_span = self._get_span_with_compounds(obj)

                        # Add the triple
                        triples.append((subj_span.text, token.lemma_, obj_span.text))

        return triples

    def _get_span_with_compounds(self, token):
        """
        Get a span that includes the token and any compound words.

        Args:
            token: A spaCy token.

        Returns:
            A spaCy span including the token and its compounds.
        """
        doc = token.doc

        # Find the start and end of the span
        start = token.i
        end = token.i + 1

        # Look for compound words before the token
        for child in token.children:
            if child.dep_ == "compound" and child.i < token.i:
                start = min(start, child.i)

        # Look for compound words after the token
        for child in token.children:
            if child.dep_ == "compound" and child.i > token.i:
                end = max(end, child.i + 1)

        return doc[start:end]

    def build_graph(self, chat_data: List[Dict[str, Any]], chat_id: str) -> nx.Graph:
        """
        Build a knowledge graph from chat data.

        Args:
            chat_data (List[Dict[str, Any]]): List of message dictionaries.
            chat_id (str): Unique identifier for the chat.

        Returns:
            nx.Graph: The constructed knowledge graph.
        """
        # Initialize a new graph
        self.graph = nx.Graph()
        self.graph.graph['chat_id'] = chat_id

        # Add a root node to ensure the graph always has at least one node
        self.graph.add_node('chat_root', type='root', label=f'Chat {chat_id[:8]}...', description='Root node')

        # Track if we've added any entities
        has_entities = False

        # Process each message
        for i, message in enumerate(chat_data):
            content = message.get('content', '')
            role = message.get('role', 'unknown')

            # Skip empty messages
            if not content.strip():
                continue

            try:
                # Extract entities
                entities = self.extract_entities(content)
                if entities:
                    has_entities = True

                # Add message node first
                message_id = f"message_{i}"
                if not self.graph.has_node(message_id):
                    self.graph.add_node(message_id,
                                       label=f"{role.capitalize()} Message {i}",
                                       type="message",
                                       role=role,
                                       content=content[:100] + "..." if len(content) > 100 else content)

                    # Connect message to root node
                    self.graph.add_edge('chat_root', message_id, type="contains")

                # Add entities to the graph
                for entity in entities:
                    entity_id = f"{entity['text']}_{entity['label']}"

                    # Add the entity if it doesn't exist
                    if not self.graph.has_node(entity_id):
                        self.graph.add_node(entity_id,
                                           label=entity['text'],
                                           type=entity['label'],
                                           mentions=1)
                    else:
                        # Increment mention count
                        self.graph.nodes[entity_id]['mentions'] += 1

                    # Add an edge between the entity and the message
                    self.graph.add_edge(entity_id, message_id, type="mentioned_in")

                # Extract relationships
                relationships = self.extract_relationships(content)

                # Add relationships to the graph
                for subj, pred, obj in relationships:
                    # Create a relationship edge
                    # Note: This is simplified and may not match entities exactly
                    for subj_entity in entities:
                        if subj in subj_entity['text']:
                            subj_id = f"{subj_entity['text']}_{subj_entity['label']}"

                            for obj_entity in entities:
                                if obj in obj_entity['text']:
                                    obj_id = f"{obj_entity['text']}_{obj_entity['label']}"

                                    # Add the relationship edge
                                    if self.graph.has_node(subj_id) and self.graph.has_node(obj_id):
                                        self.graph.add_edge(subj_id, obj_id,
                                                          type="relationship",
                                                          predicate=pred,
                                                          message_id=i)
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Error extracting entities from message {i}: {str(e)}")
                # Continue with next message
                continue

        # If no entities were found, create a simple message-based graph
        if not has_entities and len(chat_data) > 0:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"No entities found in chat {chat_id}. Creating a simple message-based graph.")

            # Add nodes for each role type
            roles = set(message.get('role', 'unknown') for message in chat_data if message.get('content', '').strip())
            for role in roles:
                role_id = f"role_{role}"
                self.graph.add_node(role_id, type='role', label=role.capitalize())
                self.graph.add_edge('chat_root', role_id, type='has_role')

                # Connect messages of this role
                for i, message in enumerate(chat_data):
                    if message.get('role') == role and message.get('content', '').strip():
                        message_id = f"message_{i}"
                        if not self.graph.has_node(message_id):
                            content = message.get('content', '')
                            self.graph.add_node(message_id,
                                               label=f"{role.capitalize()} {i}",
                                               type="message",
                                               role=role,
                                               content=content[:100] + "..." if len(content) > 100 else content)
                        self.graph.add_edge(role_id, message_id, type='contains')

        return self.graph

    def save_graph(self, chat_id: str) -> str:
        """
        Save the knowledge graph to disk.

        Args:
            chat_id (str): Unique identifier for the chat.

        Returns:
            str: Path to the saved graph file.
        """
        # Create the directory if it doesn't exist
        os.makedirs(KG_PATH, exist_ok=True)

        # Save the graph
        graph_path = os.path.join(KG_PATH, f"{chat_id}.pkl")
        with open(graph_path, 'wb') as f:
            pickle.dump(self.graph, f)

        return graph_path

    def load_graph(self, chat_id: str) -> nx.Graph:
        """
        Load a knowledge graph from disk.

        Args:
            chat_id (str): Unique identifier for the chat.

        Returns:
            nx.Graph: The loaded knowledge graph.

        Raises:
            FileNotFoundError: If the graph file doesn't exist.
        """
        graph_path = os.path.join(KG_PATH, f"{chat_id}.pkl")

        if not os.path.exists(graph_path):
            raise FileNotFoundError(f"Knowledge graph for chat {chat_id} not found.")

        with open(graph_path, 'rb') as f:
            self.graph = pickle.load(f)

        return self.graph

    def export_graph_for_vis(self, chat_id: str, format: str = "json") -> Dict[str, Any]:
        """
        Export the knowledge graph in a format suitable for visualization.

        Args:
            chat_id (str): Unique identifier for the chat.
            format (str): Export format ('json' or 'cytoscape').

        Returns:
            Dict[str, Any]: The graph data in the specified format.

        Raises:
            ValueError: If the format is not supported.
            FileNotFoundError: If the graph file doesn't exist.
        """
        import logging
        logger = logging.getLogger(__name__)

        # Try to load the graph if it's not already loaded or if it's for a different chat
        if not hasattr(self, 'graph') or self.graph.graph.get('chat_id') != chat_id:
            try:
                self.load_graph(chat_id)
                logger.info(f"Successfully loaded knowledge graph for chat {chat_id}")
            except FileNotFoundError:
                # If the graph file doesn't exist, try to build it on-the-fly
                # This is a fallback mechanism in case the graph wasn't built during upload
                logger.warning(f"Knowledge graph for chat {chat_id} not found. Attempting to build it.")

                # We need to get the chat data to build the graph
                from src.parsing import JSONParser, MarkdownParser
                import os

                # Define the upload folder path
                upload_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'raw_chats')

                # Look for the chat file
                chat_data = None
                for filename in os.listdir(upload_folder):
                    if filename.startswith(chat_id):
                        file_path = os.path.join(upload_folder, filename)
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()

                        # Parse the content based on file extension
                        if filename.endswith('.json'):
                            parser = JSONParser()
                        else:  # Default to markdown for other extensions
                            parser = MarkdownParser()

                        chat_data = parser.parse(content)
                        break

                if chat_data:
                    # Build and save the graph
                    self.build_graph(chat_data, chat_id)
                    self.save_graph(chat_id)
                    logger.info(f"Successfully built and saved knowledge graph for chat {chat_id}")
                else:
                    # If we can't find the chat data, return an empty graph
                    logger.error(f"Could not find chat data for {chat_id}")
                    if format == "json":
                        return {'nodes': [], 'links': []}
                    elif format == "cytoscape":
                        return {'elements': []}
                    else:
                        raise ValueError(f"Unsupported export format: {format}. Use 'json' or 'cytoscape'.")

        # Log graph information
        logger.info(f"Graph for chat {chat_id} has {len(self.graph.nodes)} nodes and {len(self.graph.edges)} edges")
        if len(self.graph.nodes) == 0:
            logger.warning("Graph has no nodes!")
            # Return empty structure
            if format == "json":
                return {'nodes': [], 'links': []}
            elif format == "cytoscape":
                return {'elements': []}
            else:
                raise ValueError(f"Unsupported export format: {format}. Use 'json' or 'cytoscape'.")
        if format == "json":
            # Basic JSON format with nodes and links
            nodes = []
            links = []

            for node_id in self.graph.nodes():
                node_data = self.graph.nodes[node_id]
                nodes.append({
                    'id': node_id,
                    'label': node_data.get('label', node_id),
                    'type': node_data.get('type', 'unknown'),
                    **{k: v for k, v in node_data.items() if k not in ['label', 'type']}
                })

            for source, target, edge_data in self.graph.edges(data=True):
                links.append({
                    'source': source,
                    'target': target,
                    'type': edge_data.get('type', 'unknown'),
                    **{k: v for k, v in edge_data.items() if k != 'type'}
                })

            return {
                'nodes': nodes,
                'links': links
            }

        elif format == "cytoscape":
            # Cytoscape.js format
            elements = []

            # Add nodes
            for node_id in self.graph.nodes():
                node_data = self.graph.nodes[node_id]
                elements.append({
                    'data': {
                        'id': node_id,
                        'label': node_data.get('label', node_id),
                        'type': node_data.get('type', 'unknown'),
                        **{k: v for k, v in node_data.items() if k not in ['label', 'type']}
                    }
                })

            # Add edges
            for source, target, edge_data in self.graph.edges(data=True):
                edge_id = f"{source}_{target}"
                elements.append({
                    'data': {
                        'id': edge_id,
                        'source': source,
                        'target': target,
                        'type': edge_data.get('type', 'unknown'),
                        **{k: v for k, v in edge_data.items() if k != 'type'}
                    }
                })

            return {
                'elements': elements
            }

        else:
            raise ValueError(f"Unsupported export format: {format}. Use 'json' or 'cytoscape'.")


# Module-level functions that use a singleton instance of KnowledgeGraphBuilder

_builder = None

def _get_builder() -> KnowledgeGraphBuilder:
    """
    Get or create a singleton instance of KnowledgeGraphBuilder.

    Returns:
        KnowledgeGraphBuilder: The singleton instance.
    """
    global _builder
    if _builder is None:
        _builder = KnowledgeGraphBuilder()
    return _builder

def build_graph(chat_data: List[Dict[str, Any]], chat_id: str) -> nx.Graph:
    """
    Build a knowledge graph from chat data using the singleton KnowledgeGraphBuilder.

    Args:
        chat_data (List[Dict[str, Any]]): List of message dictionaries.
        chat_id (str): Unique identifier for the chat.

    Returns:
        nx.Graph: The constructed knowledge graph.
    """
    builder = _get_builder()
    return builder.build_graph(chat_data, chat_id)

def save_graph(chat_id: str) -> str:
    """
    Save the knowledge graph to disk using the singleton KnowledgeGraphBuilder.

    Args:
        chat_id (str): Unique identifier for the chat.

    Returns:
        str: Path to the saved graph file.
    """
    builder = _get_builder()
    return builder.save_graph(chat_id)

def load_graph(chat_id: str) -> nx.Graph:
    """
    Load a knowledge graph from disk using the singleton KnowledgeGraphBuilder.

    Args:
        chat_id (str): Unique identifier for the chat.

    Returns:
        nx.Graph: The loaded knowledge graph.
    """
    builder = _get_builder()
    return builder.load_graph(chat_id)

def export_graph_for_vis(chat_id: str, format: str = "json") -> Dict[str, Any]:
    """
    Export the knowledge graph in a format suitable for visualization using the singleton KnowledgeGraphBuilder.

    Args:
        chat_id (str): Unique identifier for the chat.
        format (str): Export format ('json' or 'cytoscape').

    Returns:
        Dict[str, Any]: The graph data in the specified format.
    """
    builder = _get_builder()
    return builder.export_graph_for_vis(chat_id, format)
