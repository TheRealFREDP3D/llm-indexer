# llm-indexer

## Reviewer's Guide by Sourcery

This pull request introduces the initial project structure and core functionalities for the LLM Chat Indexer. It includes modules for parsing chat logs (JSON and Markdown), indexing chat data using ChromaDB and Sentence Transformers, building knowledge graphs using spaCy and NetworkX, semantic search, summarization using the Gemini API, and utility functions. The code also includes tests for the utils and parsing modules.

_No diagrams generated as the changes look simple and do not need a visual representation._

### File-Level Changes

| Change | Details | Files |
| ------ | ------- | ----- |
| Implemented a knowledge graph builder using spaCy and NetworkX to extract entities and relationships from chat data. | <ul><li>Initialized a spaCy model for entity recognition and dependency parsing.</li><li>Created methods to extract entities and relationships from text.</li><li>Implemented graph construction from chat data, including nodes for entities and messages, and edges for mentions and relationships.</li><li>Added functionality to save and load knowledge graphs to/from disk using pickle.</li><li>Implemented graph export in JSON and Cytoscape formats for visualization.</li><li>Implemented module-level functions to use a singleton instance of KnowledgeGraphBuilder.</li></ul> | `llm-chat-indexer/src/knowledge_graph/builder.py`<br/>`src/knowledge_graph/builder.py` |
| Implemented semantic search functionality using ChromaDB and Sentence Transformers. | <ul><li>Initialized a Sentence Transformer model for generating embeddings.</li><li>Created methods to search for relevant chunks in a specific chat collection.</li><li>Implemented search across all chat collections.</li><li>Added module-level functions to use a singleton instance of SemanticSearcher.</li></ul> | `llm-chat-indexer/src/search/semantic_search.py`<br/>`src/search/semantic_search.py` |
| Implemented text utility functions for cleaning and chunking text. | <ul><li>Created a function to clean text by removing extra whitespace and normalizing line breaks.</li><li>Implemented a function to split text into overlapping chunks for embedding.</li><li>Added a function to process a list of messages and create chunks with metadata.</li></ul> | `llm-chat-indexer/src/utils/text_utils.py`<br/>`src/utils/text_utils.py` |
| Implemented vector indexing functionality using Sentence Transformers and ChromaDB. | <ul><li>Initialized a Sentence Transformer model for generating embeddings.</li><li>Created methods to index chat data by chunking, embedding, and storing in ChromaDB.</li><li>Implemented a function to get the names of all collections in the database.</li><li>Added module-level functions to use a singleton instance of VectorIndexer.</li></ul> | `llm-chat-indexer/src/indexing/vector_indexer.py`<br/>`src/indexing/vector_indexer.py` |
| Implemented a Google Gemini API client for text generation and summarization. | <ul><li>Initialized the Gemini client with API key and model.</li><li>Created a method to generate text using the Gemini API.</li><li>Implemented a function to generate a summary of the provided text.</li><li>Added a function to extract entities from the provided text using Gemini.</li></ul> | `llm-chat-indexer/src/llm_clients/gemini_client.py`<br/>`src/llm_clients/gemini_client.py` |
| Implemented JSON and Markdown parsers for chat logs. | <ul><li>Created a JSON parser to parse chat logs in JSON format.</li><li>Implemented a Markdown parser to parse chat logs in Markdown format.</li></ul> | `llm-chat-indexer/src/parsing/json_parser.py`<br/>`src/parsing/json_parser.py`<br/>`llm-chat-indexer/src/parsing/md_parser.py`<br/>`src/parsing/md_parser.py` |
| Added tests for the utils and parsing modules. | <ul><li>Created test cases for the text_utils module.</li><li>Implemented test cases for the JSONParser and MarkdownParser classes.</li></ul> | `llm-chat-indexer/tests/test_utils.py`<br/>`tests/test_utils.py`<br/>`llm-chat-indexer/tests/test_parsing.py`<br/>`tests/test_parsing.py` |
| Implemented a distiller for generating summaries of chat data. | <ul><li>Created a function to format a list of messages into a string suitable for summarization.</li><li>Implemented a function to generate a summary of the chat data.</li></ul> | `llm-chat-indexer/src/summarization/distiller.py`<br/>`src/summarization/distiller.py` |
| Created base parser class for chat logs. | <ul><li>Created an abstract base class for chat log parsers.</li><li>Defined the parse method.</li></ul> | `llm-chat-indexer/src/parsing/base_parser.py`<br/>`src/parsing/base_parser.py` |
| Created init files for the different modules. | <ul><li>Created init file for the knowledge graph module.</li><li>Created init file for the parsing module.</li><li>Created init file for the indexing module.</li><li>Created init file for the llm clients module.</li><li>Created init file for the search module.</li><li>Created init file for the summarization module.</li><li>Created init file for the utils module.</li><li>Created init file for the src module.</li><li>Created init file for the tests module.</li></ul> | `llm-chat-indexer/src/knowledge_graph/__init__.py`<br/>`llm-chat-indexer/src/parsing/__init__.py`<br/>`src/knowledge_graph/__init__.py`<br/>`src/parsing/__init__.py`<br/>`llm-chat-indexer/src/indexing/__init__.py`<br/>`llm-chat-indexer/src/llm_clients/__init__.py`<br/>`llm-chat-indexer/src/search/__init__.py`<br/>`llm-chat-indexer/src/summarization/__init__.py`<br/>`llm-chat-indexer/src/utils/__init__.py`<br/>`src/indexing/__init__.py`<br/>`src/llm_clients/__init__.py`<br/>`src/search/__init__.py`<br/>`src/summarization/__init__.py`<br/>`src/utils/__init__.py`<br/>`llm-chat-indexer/src/__init__.py`<br/>`llm-chat-indexer/tests/__init__.py` |

---

<details>
<summary>Tips and commands</summary>

#### Interacting with Sourcery

- **Trigger a new review:** Comment `@sourcery-ai review` on the pull request.
- **Continue discussions:** Reply directly to Sourcery's review comments.
- **Generate a GitHub issue from a review comment:** Ask Sourcery to create an
  issue from a review comment by replying to it. You can also reply to a
  review comment with `@sourcery-ai issue` to create an issue from it.
- **Generate a pull request title:** Write `@sourcery-ai` anywhere in the pull
  request title to generate a title at any time. You can also comment
  `@sourcery-ai title` on the pull request to (re-)generate the title at any time.
- **Generate a pull request summary:** Write `@sourcery-ai summary` anywhere in
  the pull request body to generate a PR summary at any time exactly where you
  want it. You can also comment `@sourcery-ai summary` on the pull request to
  (re-)generate the summary at any time.
- **Generate reviewer's guide:** Comment `@sourcery-ai guide` on the pull
  request to (re-)generate the reviewer's guide at any time.
- **Resolve all Sourcery comments:** Comment `@sourcery-ai resolve` on the
  pull request to resolve all Sourcery comments. Useful if you've already
  addressed all the comments and don't want to see them anymore.
- **Dismiss all Sourcery reviews:** Comment `@sourcery-ai dismiss` on the pull
  request to dismiss all existing Sourcery reviews. Especially useful if you
  want to start fresh with a new review - don't forget to comment
  `@sourcery-ai review` to trigger a new review!
- **Generate a plan of action for an issue:** Comment `@sourcery-ai plan` on
  an issue to generate a plan of action for it.

#### Customizing Your Experience

Access your [dashboard](https://app.sourcery.ai) to.
- Enable or disable review features such as the Sourcery-generated pull request
  summary, the reviewer's guide, and others.
- Change the review language.
- Add, remove or edit custom review instructions.
- Adjust other review settings.

#### Getting Help

- [Contact our support team](mailto:support@sourcery.ai) for questions or feedback.
- Visit our [documentation](https://docs.sourcery.ai) for detailed guides and information.
- Keep in touch with the Sourcery team by following us on [X/Twitter](https://x.com/SourceryAI), [LinkedIn](https://www.linkedin.com/company/sourcery-ai/) or [GitHub](https://github.com/sourcery-ai).

</details>

<!-- Generated by sourcery-ai[bot]: end review_guide -->