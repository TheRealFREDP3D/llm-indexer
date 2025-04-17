# Setup Guide for LLM Chat Indexer

This guide provides detailed instructions for setting up and running the LLM Chat Indexer application.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+**: The application requires Python 3.8 or higher.
- **pip**: The Python package installer.
- **git**: For cloning the repository (optional).
- **Google Gemini API key**: Required for summarization and entity extraction features.

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/llm-chat-indexer.git
cd llm-chat-indexer
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to avoid conflicts with other Python packages.

#### On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

#### On macOS/Linux:

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

#### For Production:

```bash
pip install -r requirements.txt
```

#### For Development:

```bash
pip install -r requirements-dev.txt
```

### 4. Download Spacy Language Model

```bash
python -m spacy download en_core_web_sm
```

### 5. Configure Environment Variables

1. Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

2. Edit the `.env` file and add your API keys and configuration settings:

```
# Environment variables for LLM Chat Indexer

# Paths for data storage
VECTOR_STORE_PATH=./data/vector_store
KG_PATH=./data/knowledge_graphs

# API Keys (required for certain features)
GEMINI_API_KEY=your_gemini_api_key_here

# Model settings
SENTENCE_TRANSFORMER_MODEL=all-MiniLM-L6-v2
TOP_K_RESULTS=5
```

### 6. Validate Configuration

Run the configuration validation script to ensure everything is set up correctly:

```bash
python scripts/validate_config.py
```

## Running the Application

### 1. Start ChromaDB Server (Optional)

For better performance, you can run ChromaDB as a separate server:

```bash
python scripts/start_chroma.py
```

### 2. Run the Web Application

```bash
python run.py
```

The application will be available at `http://localhost:5000`.

## Troubleshooting

### Common Issues

#### 1. Missing Dependencies

If you encounter errors about missing packages, try reinstalling the requirements:

```bash
pip install -r requirements.txt --force-reinstall
```

#### 2. API Key Issues

If summarization or entity extraction features aren't working, check that your Gemini API key is correctly set in the `.env` file.

#### 3. ChromaDB Connection Issues

If you're having trouble connecting to ChromaDB:

- Ensure the ChromaDB server is running (if using the server mode)
- Check the `CHROMA_SERVER_HOST` and `CHROMA_SERVER_HTTP_PORT` settings
- Try using the embedded mode by not starting the ChromaDB server

#### 4. File Permission Issues

If you encounter permission errors when writing to data directories:

- Check that the application has write permissions to the `data` directory
- Ensure the paths in `.env` are accessible to the application

## Development Setup

For development, additional tools are available:

### Running Tests

```bash
# Run all tests
python run_tests.py

# Run specific test modules
python run_tests.py --module test_parsing

# Run with coverage report
python run_tests.py --coverage
```

### Code Formatting

```bash
# Format code with Black
black .

# Sort imports with isort
isort .

# Check code quality with flake8
flake8 .
```

## Next Steps

After setting up the application, you can:

1. Upload chat files in JSON or Markdown format
2. Search across your indexed chats
3. Generate summaries of conversations
4. Explore knowledge graphs of entities and relationships

Refer to the [README.md](README.md) for more detailed usage instructions.
