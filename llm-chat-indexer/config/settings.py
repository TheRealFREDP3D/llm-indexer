import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Data storage paths
VECTOR_STORE_PATH = os.getenv('VECTOR_STORE_PATH', './data/vector_store')
KG_PATH = os.getenv('KG_PATH', './data/knowledge_graphs')

# Ensure paths are absolute
if not os.path.isabs(VECTOR_STORE_PATH):
    VECTOR_STORE_PATH = os.path.join(BASE_DIR, VECTOR_STORE_PATH)

if not os.path.isabs(KG_PATH):
    KG_PATH = os.path.join(BASE_DIR, KG_PATH)

# API Keys
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Application constants
SENTENCE_TRANSFORMER_MODEL = 'all-MiniLM-L6-v2'  # Default model for embeddings
CHUNK_SIZE = 1000  # Default chunk size for text splitting
CHUNK_OVERLAP = 200  # Default overlap between chunks
TOP_K_RESULTS = 5  # Default number of results to return in search

# Ensure data directories exist
os.makedirs(VECTOR_STORE_PATH, exist_ok=True)
os.makedirs(KG_PATH, exist_ok=True)
