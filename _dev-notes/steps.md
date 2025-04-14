# Step-by-Step Guide: LLM Chat Indexer Refactor

This guide outlines the steps to build the LLM Chat Indexer based on the project description.

## 1. Understand the Goal

*   **Review Vision:** Familiarize yourself with the project's goal: transforming chat logs into a searchable, summarizable knowledge base with a knowledge graph visualization.
*   **Core Principles:** Keep the modular, API-first architecture in mind. Use Python and leverage appropriate libraries.
*   **Data Flow:** Understand the sequence: Files -> Parse -> Standardize -> Index/Summarize/Build Graph -> Store -> API -> UI.

## 2. Set Up the Project Environment

*   **Create Directories:** Set up the folder structure as defined in the description (`llm-chat-indexer/`, `config/`, `data/`, `src/`, `static/`, `templates/`, `tests/`, etc.).
*   **Define Dependencies:** Create the `requirements.txt` file and list all necessary libraries (Flask, sentence-transformers, chromadb-client, spaCy, networkx, google-generativeai, python-dotenv, pytest).
*   **Install Dependencies:** Run `pip install -r requirements.txt`. Remember to download the spaCy model: `python -m spacy download en_core_web_sm`.
*   **Configure Environment:**
    *   Create a `.env` file for sensitive information like API keys and paths (`VECTOR_STORE_PATH`, `KG_PATH`). Add `.env` and `data/` to your `.gitignore`.
    *   Create `config/settings.py` to load variables from `.env` using `python-dotenv` and define application constants.

## 3. Implement Core Logic Modules (in `src/`)

*   **Parsing (`src/parsing/`):**
    *   Define `BaseParser` abstract class in `base_parser.py` with a `parse` method.
    *   Implement concrete parsers (e.g., `json_parser.py`, `md_parser.py`) inheriting from `BaseParser` to handle specific formats and return standardized message lists.
*   **Utilities (`src/utils/text_utils.py`):**
    *   Implement text cleaning functions.
    *   Implement text chunking strategies needed for effective embedding.
*   **Indexing (`src/indexing/vector_indexer.py`):**
    *   Initialize the sentence-transformer model and ChromaDB client using settings from `config/settings.py`.
    *   Implement `index_chat(chat_data, chat_id)`: Takes parsed data, chunks it using `text_utils`, generates embeddings, and stores chunks, embeddings, and metadata in ChromaDB.
*   **Search (`src/search/semantic_search.py`):**
    *   Initialize the *same* sentence-transformer model and ChromaDB client.
    *   Implement `search(query, top_n)`: Generates query embedding, queries ChromaDB for similar chunks, and returns results with metadata.
*   **LLM Clients (`src/llm_clients/`):**
    *   Create wrapper classes (e.g., `gemini_client.py`) to interact with LLM APIs.
    *   Handle authentication (using keys from settings) and provide consistent methods like `generate_summary(text)`.
*   **Summarization (`src/summarization/distiller.py`):**
    *   Use an LLM client from `src/llm_clients`.
    *   Implement `generate_summary(chat_data, summary_type)`: Constructs prompts based on `summary_type` ('gist', 'key_points'), sends content to the LLM, and returns the summary.
*   **Knowledge Graph (`src/knowledge_graph/builder.py`):**
    *   Initialize spaCy (with model) and NetworkX.
    *   Implement `build_graph(chat_data, chat_id)`: Use spaCy NER on messages, extract entities and relationships, and build a NetworkX graph.
    *   Implement `save_graph`, `load_graph`, and `export_graph_for_vis` helper functions.

## 4. Build the Web User Interface (Flask)

*   **Initialize App (`run.py`):**
    *   Set up the Flask application instance.
    *   Load configuration from `config/settings.py`.
    *   Define the main execution block to run the development server.
*   **Define Routes:**
    *   `/`: Display indexed chats, provide an indexing mechanism (calling `vector_indexer.index_chat`), include a search bar.
    *   `/search`: Handle search queries (calling `semantic_search.search`), render results.
    *   `/chat/<chat_id>`: Display full chat, add buttons/sections to trigger and show summaries (calling `distiller.generate_summary`) and the knowledge graph (using `builder` functions).
    *   (Optional) `/api/graph/<chat_id>`: Endpoint to fetch graph data as JSON.
*   **Create HTML Templates (`templates/`):**
    *   `base.html`: Common structure, CSS links.
    *   `index.html`: Homepage layout.
    *   `search_results.html`: Display search hits.
    *   `chat_view.html`: Show full chat, summary sections, and a container for the graph visualization.
*   **Add Static Files (`static/`):**
    *   Create `static/css/main.css` for styling.
    *   Include JavaScript libraries (e.g., vis.js, d3.js) if needed for graph visualization and potentially AJAX calls.

## 5. Integrate and Test

*   **Connect Components:** Ensure Flask routes correctly invoke the functions in the `src/` modules.
*   **Test Workflow:**
    *   Index various chat logs.
    *   Perform semantic searches.
    *   View individual chats.
    *   Generate summaries (gist, key points).
    *   Visualize knowledge graphs.
*   **Write Formal Tests (`tests/`):** Implement unit tests for individual functions (parsing, chunking, embedding, etc.) and integration tests for key workflows (indexing-to-search).

## 6. (Future) Plan for API Extensibility

*   **Review API Needs:** Consider the core functions needed for external integrations (like an IDE plugin): `index_file`, `semantic_search`, `get_summary`, `get_graph_data`, `get_full_chat`.
*   **Design API Endpoints:** Plan dedicated Flask routes (e.g., under `/api/`) that wrap the core service functions and return data in standard formats like JSON.
