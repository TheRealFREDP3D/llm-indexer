@echo off
REM Create directory structure
mkdir llm-chat-indexer\config
mkdir llm-chat-indexer\data\raw_chats
mkdir llm-chat-indexer\data\vector_store
mkdir llm-chat-indexer\data\knowledge_graphs
mkdir llm-chat-indexer\notebooks
mkdir llm-chat-indexer\src\parsing
mkdir llm-chat-indexer\src\indexing
mkdir llm-chat-indexer\src\search
mkdir llm-chat-indexer\src\summarization
mkdir llm-chat-indexer\src\knowledge_graph
mkdir llm-chat-indexer\src\llm_clients
mkdir llm-chat-indexer\src\utils
mkdir llm-chat-indexer\static\css
mkdir llm-chat-indexer\templates
mkdir llm-chat-indexer\tests

REM Create empty files
type nul > llm-chat-indexer\.env
type nul > llm-chat-indexer\.gitignore
type nul > llm-chat-indexer\requirements.txt
type nul > llm-chat-indexer\run.py
type nul > llm-chat-indexer\config\settings.py
type nul > llm-chat-indexer\static\css\main.css
type nul > llm-chat-indexer\templates\base.html
type nul > llm-chat-indexer\templates\index.html
type nul > llm-chat-indexer\templates\search_results.html
type nul > llm-chat-indexer\templates\chat_view.html

echo Project structure created successfully!
