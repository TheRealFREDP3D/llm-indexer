# LLM Chat Indexer

A powerful tool for transforming raw LLM chat logs into an intelligent, multi-faceted knowledge base. This project enables semantic search, summarization, and knowledge graph visualization of your chat data.

![LLM Chat Indexer](https://via.placeholder.com/800x400?text=LLM+Chat+Indexer)

## 🌟 Features

- **Multi-format Parsing**: Support for JSON and Markdown chat logs
- **Semantic Search**: Find relevant information across your chat history using natural language queries
- **Summarization**: Generate concise summaries of chat conversations using Google's Gemini API
- **Knowledge Graph**: Visualize conceptual connections between entities mentioned in chats
- **Web Interface**: User-friendly interface for uploading, searching, and exploring chat data
- **API-First Design**: Core functionality accessible via API for integration with other tools

## 🏗️ Architecture

The project follows a modular, API-first architecture:

- **Core Logic**: Parsing, indexing, search, summarization, and graph generation are independent of the presentation layer
- **Data Flow**: Files → Parse → Standardized Format → Index/Summarize/Build Graph → Store → Query/Visualize via API → Present in UI
- **Technology**: Python-centric, leveraging powerful libraries for NLP, vector search, graph analysis, and web development

## 📁 Project Structure

```text
llm-chat-indexer/
├── .env                  # Environment variables (API keys, paths)
├── .gitignore
├── config/
│   └── settings.py       # Configuration loading and constants
├── data/                 # Default storage for indexes, graphs, etc.
│   ├── raw_chats/        # Place raw chat logs here
│   ├── vector_store/     # ChromaDB index files
│   └── knowledge_graphs/ # Saved graph files
├── notebooks/            # Jupyter notebooks for experimentation
├── requirements.txt      # Project dependencies
├── run.py                # Main entry point to start the web server
├── src/
│   ├── __init__.py
│   ├── parsing/          # Handles different chat log formats
│   │   ├── __init__.py
│   │   ├── base_parser.py
│   │   ├── json_parser.py
│   │   └── md_parser.py
│   ├── indexing/         # Text indexing and vector embedding
│   │   ├── __init__.py
│   │   └── vector_indexer.py
│   ├── search/           # Search logic (semantic)
│   │   ├── __init__.py
│   │   └── semantic_search.py
│   ├── summarization/    # Chat summarization logic
│   │   ├── __init__.py
│   │   └── distiller.py
│   ├── knowledge_graph/  # Knowledge graph generation
│   │   ├── __init__.py
│   │   └── builder.py
│   ├── llm_clients/      # Abstraction for interacting with LLMs
│   │   ├── __init__.py
│   │   └── gemini_client.py
│   └── utils/            # Shared utility functions
│       ├── __init__.py
│       └── text_utils.py
├── static/               # Static assets for web interface
│   └── css/
├── templates/            # HTML templates for web interface
└── tests/                # Unit and integration tests
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/llm-chat-indexer.git
   cd llm-chat-indexer
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Download the spaCy model:

   ```bash
   python -m spacy download en_core_web_sm
   ```

5. Create a `.env` file in the project root with your API keys:

   ```env
   GEMINI_API_KEY=your_gemini_api_key
   VECTOR_STORE_PATH=./data/vector_store
   KG_PATH=./data/knowledge_graphs
   ```

## 🔧 Usage

### Running the Web Interface

1. Start the Flask application:

   ```bash
   python run.py
   ```

2. Open your browser and navigate to `http://localhost:5000`

3. Upload chat logs (JSON or Markdown format)

4. Use the search functionality to find relevant information

5. View chat details, summaries, and knowledge graphs

### Supported Chat Formats

#### JSON Format

```json
[
  {
    "role": "user",
    "content": "Hello, how can you help me with my project?"
  },
  {
    "role": "assistant",
    "content": "I can help you by providing information, generating code, and answering questions about your project."
  }
]
```

#### Markdown Format

```markdown
# User
Hello, how can you help me with my project?

# Assistant
I can help you by providing information, generating code, and answering questions about your project.
```

## 📊 Core Components

### Parsing

The system supports parsing chat logs in JSON and Markdown formats, converting them into a standardized internal representation.

### Indexing

Chat data is chunked, embedded using Sentence Transformers, and stored in ChromaDB for efficient retrieval.

### Semantic Search

Search functionality uses the same embedding model to find semantically relevant chunks across all indexed chats.

### Summarization

The Gemini API is used to generate concise summaries of chat conversations, extracting key points and insights.

### Knowledge Graph

spaCy and NetworkX are used to extract entities and relationships from chats, creating a navigable knowledge graph.

## 🔌 API Reference

### Main Endpoints

- **GET /** - Home page with upload form and list of indexed chats
- **POST /upload** - Upload and index a new chat file
- **GET /search** - Search indexed chats with a query parameter
- **GET /chat/{chat_id}** - View a specific chat with options for summary and knowledge graph
- **GET /api/summary/{chat_id}** - Get a summary of a specific chat
- **GET /api/graph/{chat_id}** - Get knowledge graph data for a specific chat

## 🤝 Contributing

Contributions are welcome! Here are some ways you can contribute:

1. Report bugs and suggest features by opening issues
2. Submit pull requests with bug fixes or new features
3. Improve documentation
4. Add support for new chat formats
5. Enhance the web interface

Please follow these steps for contributing:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Run tests to ensure they pass
5. Commit your changes (`git commit -m 'Add some feature'`)
6. Push to the branch (`git push origin feature/your-feature`)
7. Open a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [Sentence Transformers](https://www.sbert.net/) for text embeddings
- [ChromaDB](https://www.trychroma.com/) for vector storage
- [spaCy](https://spacy.io/) for NLP processing
- [NetworkX](https://networkx.org/) for graph operations
- [Google Generative AI](https://ai.google.dev/) for the Gemini API
- [Flask](https://flask.palletsprojects.com/) for the web framework
