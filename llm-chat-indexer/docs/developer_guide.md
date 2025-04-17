# LLM Chat Indexer Developer Guide

This guide provides detailed information for developers who want to understand, modify, or extend the LLM Chat Indexer application.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Module Descriptions](#module-descriptions)
- [Development Workflow](#development-workflow)
- [Adding New Features](#adding-new-features)
- [Testing](#testing)
- [API Reference](#api-reference)
- [Deployment](#deployment)

## Architecture Overview

### High-Level Architecture

The LLM Chat Indexer is built with a modular architecture:

1. **Web Interface**: Flask-based web application for user interaction
2. **Parsing Module**: Converts different file formats into a standardized message format
3. **Indexing Module**: Stores and indexes chat data using vector embeddings
4. **Search Module**: Provides semantic search functionality across indexed chats
5. **Knowledge Graph Module**: Extracts entities and relationships from chats
6. **Summarization Module**: Generates summaries of chat conversations
7. **Configuration Module**: Manages application settings and environment variables

### Data Flow

1. User uploads a chat file (JSON or Markdown)
2. The parsing module converts the file into a standardized message format
3. The indexing module chunks the messages, generates embeddings, and stores them in ChromaDB
4. The knowledge graph module extracts entities and relationships and builds a graph
5. Users can search across indexed chats using the search module
6. Users can generate summaries using the summarization module
7. Users can explore knowledge graphs using the visualization interface

## Module Descriptions

### Parsing Module (`src/parsing/`)

The parsing module is responsible for converting different file formats into a standardized message format.

- `base_parser.py`: Defines the abstract base class for parsers
- `json_parser.py`: Implements parsing for JSON files
- `md_parser.py`: Implements parsing for Markdown files

### Indexing Module (`src/indexing/`)

The indexing module handles storing and indexing chat data using vector embeddings.

- `vector_indexer.py`: Implements vector indexing using ChromaDB and sentence transformers

### Search Module (`src/search/`)

The search module provides semantic search functionality across indexed chats.

- `semantic_search.py`: Implements semantic search using vector embeddings

### Knowledge Graph Module (`src/knowledge_graph/`)

The knowledge graph module extracts entities and relationships from chats and builds a graph.

- `builder.py`: Implements knowledge graph construction
- `extractor.py`: Implements entity and relationship extraction

### Summarization Module (`src/summarization/`)

The summarization module generates summaries of chat conversations.

- `distiller.py`: Implements chat summarization using the Gemini API

### LLM Clients Module (`src/llm_clients/`)

The LLM clients module provides interfaces to different language model APIs.

- `gemini_client.py`: Implements a client for the Google Gemini API

### Utilities Module (`src/utils/`)

The utilities module provides common functionality used across the application.

- `text_utils.py`: Implements text processing utilities

### Configuration Module (`config/`)

The configuration module manages application settings and environment variables.

- `config.py`: Implements the Configuration class
- `settings.py`: Exports configuration values as module-level variables

### Web Interface (`run.py`, `templates/`, `static/`)

The web interface provides a user-friendly way to interact with the application.

- `run.py`: Implements the Flask application and routes
- `templates/`: Contains HTML templates for the web interface
- `static/`: Contains static assets (CSS, JavaScript, images)

## Development Workflow

### Setting Up the Development Environment

1. Clone the repository
2. Create and activate a virtual environment
3. Install development dependencies: `pip install -r requirements-dev.txt`
4. Set up environment variables in a `.env` file
5. Run the application: `python run.py`

### Code Style and Conventions

- Follow PEP 8 for Python code style
- Use Google-style docstrings for all functions, classes, and modules
- Use type hints for function parameters and return values
- Use meaningful variable and function names
- Keep functions small and focused on a single responsibility
- Write tests for all new functionality

### Version Control

- Use Git for version control
- Create feature branches for new features or bug fixes
- Write clear, descriptive commit messages
- Submit pull requests for code review
- Ensure all tests pass before merging

## Adding New Features

### Adding a New Parser

To add support for a new file format:

1. Create a new parser class in `src/parsing/` that extends `BaseParser`
2. Implement the `parse` method to convert the file format into the standardized message format
3. Update the file upload handler in `run.py` to use the new parser
4. Add tests for the new parser in `tests/test_parsing.py`

### Adding a New LLM Client

To add support for a new language model API:

1. Create a new client class in `src/llm_clients/` (e.g., `openai_client.py`)
2. Implement the required methods (e.g., `generate_text`, `generate_summary`, `extract_entities`)
3. Update the configuration to include the new API key
4. Add tests for the new client in `tests/test_llm_clients.py`

### Adding a New API Endpoint

To add a new API endpoint:

1. Add the endpoint to `run.py`
2. Update the Swagger documentation in `src/api/swagger.py`
3. Update the API documentation in `API.md`
4. Add tests for the new endpoint

## Testing

### Running Tests

```bash
# Run all tests
python run_tests.py

# Run specific test modules
python run_tests.py --module test_parsing

# Run with coverage report
python run_tests.py --coverage
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files with the prefix `test_`
- Name test functions with the prefix `test_`
- Use descriptive test names that explain what is being tested
- Use fixtures from `conftest.py` where appropriate

### Test Coverage

Aim for high test coverage, especially for critical functionality:
- Parsing module: 100% coverage
- Indexing module: 90%+ coverage
- Search module: 90%+ coverage
- API endpoints: 80%+ coverage

## API Reference

See the [API Documentation](../API.md) for detailed information about the API endpoints.

### Swagger Documentation

The application provides Swagger documentation at `/api/docs` when running.

## Deployment

### Production Deployment

For production deployment:

1. Set `debug=False` in `run.py`
2. Use a production WSGI server (e.g., Gunicorn, uWSGI)
3. Set up a reverse proxy (e.g., Nginx, Apache)
4. Set up SSL/TLS for secure connections
5. Configure proper logging
6. Set up monitoring and alerting

### Docker Deployment

A Dockerfile is provided for containerized deployment:

```bash
# Build the Docker image
docker build -t llm-chat-indexer .

# Run the container
docker run -p 5000:5000 -v ./data:/app/data llm-chat-indexer
```

### Environment Variables

Set the following environment variables for production:

- `FLASK_ENV=production`
- `ALLOW_RESET=False`
- `GEMINI_API_KEY=your_api_key`
- `VECTOR_STORE_PATH=/path/to/persistent/storage`
- `KG_PATH=/path/to/persistent/storage`

## Performance Optimization

### Vector Indexing

- Use a dedicated ChromaDB server for better performance
- Adjust chunk size and overlap based on your specific use case
- Consider using a more powerful embedding model for better search results

### Knowledge Graph Generation

- Entity extraction can be slow for large chats
- Consider implementing caching for extracted entities
- Use a more efficient graph database for very large graphs

### Web Interface

- Implement pagination for large result sets
- Use AJAX for asynchronous operations
- Optimize static assets (minify CSS/JS, compress images)
