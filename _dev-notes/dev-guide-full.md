# Development Guide: LLM Chat Indexer Refactor

## I. Vision & Core Principles

*   **Goal:** Transform raw LLM chat logs into an intelligent, multi-faceted knowledge base. Users should be able to search semantically, get condensed insights (summaries), and visualize conceptual connections (knowledge graph).
*   **Architecture:** Modular, API-first. Core logic (parsing, indexing, search, summarization, graph generation) should be independent of the presentation layer (Web UI, future IDE plugin). This ensures reusability and testability.
*   **Technology:** Python-centric. Leverage powerful libraries for NLP, vector search, graph analysis, and web development.
*   **Data Flow:** Files -> Parse -> Standardized Format -> Index (Text + Vectors) / Summarize / Build Graph -> Store -> Query/Visualize via API -> Present in UI.

## II. Project Setup

1.  **Directory Structure:**

    ```
    llm-chat-indexer/
    ├── .env                  # Environment variables (API keys, paths)
    ├── .gitignore
    ├── config/
    │   └── settings.py       # Configuration loading and constants
    ├── data/                 # Default storage for indexes, graphs, etc. (add to .gitignore)
    │   ├── raw_chats/        # (Optional) Place raw chat logs here
    │   ├── vector_store/     # ChromaDB or FAISS index files
    │   └── knowledge_graphs/ # Saved graph files (e.g., GraphML)
    ├── notebooks/            # Jupyter notebooks for experimentation (optional)
    ├── requirements.txt      # Project dependencies
    ├── run.py                # Main entry point to start the web server
    ├── src/
    │   ├── __init__.py
    │   ├── parsing/          # Handles different chat log formats
    │   │   ├── __init__.py
    │   │   ├── base_parser.py
    │   │   └── ... (e.g., json_parser.py, md_parser.py)
    │   ├── indexing/         # Text indexing and vector embedding
    │   │   ├── __init__.py
    │   │   └── vector_indexer.py
    │   ├── search/           # Search logic (keyword + semantic)
    │   │   ├── __init__.py
    │   │   └── semantic_search.py
    │   ├── summarization/    # Chat Distiller logic
    │   │   ├── __init__.py
    │   │   └── distiller.py
    │   ├── knowledge_graph/  # KG generation
    │   │   ├── __init__.py
    │   │   └── builder.py
    │   ├── llm_clients/      # Abstraction for interacting with different LLMs
    │   │   ├── __init__.py
    │   │   └── ... (e.g., gemini_client.py, openai_client.py)
    │   └── utils/            # Shared utility functions (e.g., chunking)
    │       ├── __init__.py
    │       └── text_utils.py
    ├── static/               # CSS, JavaScript for web UI
    │   └── css/
    │       └── main.css
    ├── templates/            # HTML templates for web UI
    │   ├── base.html
    │   ├── index.html
    │   ├── search_results.html
    │   └── chat_view.html
    └── tests/                # Unit and integration tests
        ├── ...
    ```

2.  **Dependencies (`requirements.txt`):**

    ```txt
    # Core Framework
    flask

    # Vector Search & Embeddings
    sentence-transformers
    chromadb-client # Or faiss-cpu / faiss-gpu if using FAISS

    # NLP & Knowledge Graph
    spacy # Or nltk
    # python -m spacy download en_core_web_sm # Run this after installing spacy
    networkx

    # LLM Interaction (Choose based on preference)
    google-generativeai # For Gemini
    # openai # For OpenAI models

    # Utilities
    python-dotenv
    langchain # (Optional) Can help orchestrate many of these steps

    # Testing
    pytest
    ```

3.  **Configuration (`config/settings.py`, `.env`):**
    *   Use `python-dotenv` to load API keys (GEMINI_API_KEY, OPENAI_API_KEY, etc.), paths (`VECTOR_STORE_PATH`, `KG_PATH`), model names (`EMBEDDING_MODEL_NAME`, `SUMMARIZATION_MODEL_NAME`), etc., from the `.env` file.
    *   `settings.py` should load these variables and provide constants for use throughout the application.

## III. Module Implementation Details

1.  **`src/parsing`:**
    *   `base_parser.py`: Define an abstract base class with a `parse(file_path)` method that returns a standardized list of message objects (e.g., `[{'role': 'user'/'assistant', 'content': '...', 'timestamp': ...}, ...]`).
    *   Implement concrete parsers for each supported format (JSON, Markdown, potentially others) inheriting from `BaseParser`.

2.  **`src/utils/text_utils.py`:**
    *   Implement text cleaning functions.
    *   Implement chunking strategies (e.g., chunk by turn pairs, overlapping windows by sentence/token count) crucial for effective embedding.

3.  **`src/indexing/vector_indexer.py`:**
    *   Initialize the `sentence-transformers` model (from `settings`).
    *   Initialize the vector store client (ChromaDB recommended for ease of setup). Connect to the path defined in `settings`. Create a collection if it doesn't exist.
    *   `index_chat(chat_data: list, chat_id: str)` function:
        *   Takes the parsed chat data (list of messages).
        *   Uses `text_utils` to chunk the conversation into meaningful segments.
        *   Generates embeddings for each chunk using the sentence transformer model.
        *   Stores the chunks, their embeddings, and metadata (chat\_id, chunk\_index, potentially timestamp) in the ChromaDB collection. Ensure `chat_id` and `chunk_index` allow easy retrieval later.

4.  **`src/search/semantic_search.py`:**
    *   Initialize the *same* `sentence-transformers` model used for indexing.
    *   Initialize the vector store client.
    *   `search(query: str, top_n: int = 5)` function:
        *   Generates an embedding for the user's `query`.
        *   Queries the ChromaDB collection using the query embedding to find the `top_n` most similar chunks based on cosine similarity.
        *   Returns the retrieved chunks along with their metadata and similarity scores.

5.  **`src/llm_clients`:**
    *   Create wrapper classes for different LLM APIs (e.g., Gemini, OpenAI).
    *   These classes should handle authentication (using API keys from `settings`), request formatting, and response parsing.
    *   Provide consistent methods like `generate_text(prompt)` or `generate_summary(text)`.

6.  **`src/summarization/distiller.py`:**
    *   Uses an LLM client (from `src/llm_clients`).
    *   `generate_summary(chat_data: list, summary_type: str = 'gist')` function:
        *   Selects the appropriate LLM based on `settings`.
        *   Constructs a specific prompt based on `summary_type`:
            *   **'gist':** "Provide a one-sentence summary of the following conversation:"
            *   **'key_points':** "Extract the main problems discussed and their solutions/key decisions from this conversation as a bulleted list:"
            *   **'structured':** (More advanced) Potentially identify problem statements, proposed solutions, final outcomes. Might require multiple LLM calls or more sophisticated prompting.
        *   Sends the formatted chat content and prompt to the LLM client.
        *   Returns the generated summary text.

7.  **`src/knowledge_graph/builder.py`:**
    *   Initialize an NLP pipeline (spaCy recommended). Load a model (e.g., `en_core_web_sm`). You might need to add custom entity recognition rules for specific libraries, functions, or error codes.
    *   Initialize NetworkX for graph manipulation.
    *   `build_graph(chat_data: list, chat_id: str)` function:
        *   Iterate through messages in `chat_data`.
        *   Use spaCy for Named Entity Recognition (NER) to identify relevant entities (people, organizations, code elements, libraries, concepts, potential errors).
        *   Implement rules or simple relation extraction logic to identify relationships between entities within or across messages (e.g., "User mentions LibraryX", "Assistant suggests FunctionY for ProblemZ", "ErrorA occurs after using MethodB").
        *   Add entities as nodes and relationships as edges to a NetworkX graph object. Store relevant text snippets or message IDs as node/edge attributes.
    *   `save_graph(graph, chat_id)`: Saves the NetworkX graph to a file (e.g., GraphML) in the `data/knowledge_graphs` directory.
    *   `load_graph(chat_id)`: Loads a previously saved graph.
    *   `export_graph_for_vis(graph)`: Exports the graph data in a format suitable for front-end visualization libraries (like JSON Graph Format).

## IV. Web UI (Flask Application)

1.  **`run.py`:** Initializes the Flask app, loads configuration, and starts the development server.
2.  **Routes (within `run.py` or a dedicated `web/routes.py`):**
    *   `/`: Main page. Lists indexed chats. Provides an upload/selection mechanism to index new chats. Calls `vector_indexer.index_chat`.
    *   `/search`: Handles search requests. Takes a query parameter. Calls `semantic_search.search`. Renders `search_results.html` with the results (linking to chat views). Include options for semantic vs. keyword search.
    *   `/chat/<chat_id>`: Displays a specific chat.
        *   Retrieves the full chat content (needs a simple way to store/retrieve original chats, maybe alongside the index).
        *   Provides buttons/sections to trigger and display:
            *   Gist Summary (calls `distiller.generate_summary(..., summary_type='gist')`).
            *   Key Points Summary (calls `distiller.generate_summary(..., summary_type='key_points')`).
            *   Knowledge Graph (calls `builder.load_graph`, `builder.export_graph_for_vis`, sends data to the template).
        *   Renders `chat_view.html`.
    *   `/api/graph/<chat_id>` (Optional): An API endpoint to fetch the graph data as JSON for dynamic visualization.
3.  **Templates (`templates/`):**
    *   `base.html`: Basic HTML structure, includes CSS, common header/footer.
    *   `index.html`: Lists chats, provides indexing options, search bar.
    *   `search_results.html`: Displays search results (snippets, links).
    *   `chat_view.html`: Displays the full chat transcript. Includes areas for summaries. Contains a placeholder `div` and JavaScript to render the knowledge graph using a library like `vis.js`, `d3.js`, or `sigma.js` (fed by the graph data).
4.  **Static Files (`static/`):**
    *   `main.css`: Basic styling.
    *   JavaScript for graph visualization (if needed) and potentially AJAX calls for summaries/graphs.

## V. API Design for Extensibility (Future IDE Integration)

*   **Core Principle:** The Flask routes should primarily act as thin wrappers around the core functions in `src/`.
*   **Key Functions to Expose (Conceptually):**
    *   `index_file(file_path: str) -> str`: Indexes a file, returns chat ID.
    *   `semantic_search(query: str, top_n: int) -> list[dict]`: Performs search, returns list of results (chunk text, metadata, score).
    *   `get_summary(chat_id: str, summary_type: str) -> str`: Gets a specific summary.
    *   `get_graph_data(chat_id: str) -> dict`: Gets graph data in JSON format.
    *   `get_full_chat(chat_id: str) -> list[dict]`: Retrieves the original parsed chat.
*   **How:** An IDE extension could potentially bundle the `src/` code or interact with a locally running instance of this application via HTTP requests to dedicated API endpoints (like `/api/search`, `/api/summary`, etc.) that you would add to Flask.

## VI. UI Description Summary

*   **Homepage:** Clean list of indexed conversations (by filename or title). A prominent button/area to "Index New Chat(s)". A persistent search bar.
*   **Search Results Page:** Clearly displays the search query. Lists results as cards/snippets showing the relevant chunk of text, which conversation it came from, and a similarity score (for semantic search). Each result links to the full chat view. Option to toggle between semantic/keyword search.
*   **Chat View Page:**
    *   Top: Chat title/filename.
    *   Main Area: Scrollable view of the full conversation, clearly distinguishing user/assistant messages.
    *   Side Panel/Tabs:
        *   **Summaries:** Buttons ("Gist", "Key Points") that trigger generation and display the corresponding summary below.
        *   **Knowledge Graph:** A dedicated area where the interactive graph visualization is rendered. Nodes represent entities, edges represent relationships. Hovering/clicking could show more details.
