"""
Configuration file for NeoStats AI chatbot.
All API keys and settings are managed here as environment variables.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

# ==================== LLM API Keys ====================
# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Groq Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")

# Google Gemini Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# ==================== RAG & Embeddings Configuration ====================
# Embedding Model Provider (huggingface, openai, cohere)
EMBEDDING_MODEL_PROVIDER = os.getenv("EMBEDDING_MODEL_PROVIDER", "huggingface")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")

# Vector Database Configuration (currently using FAISS for local storage)
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./data/vector_db")
DOCUMENTS_PATH = os.getenv("DOCUMENTS_PATH", "./data/documents")

# Chunk settings for RAG
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))

# ==================== Web Search Configuration ====================
# Google Search API (for web search functionality)
GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY", "")
GOOGLE_SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID", "")

# ==================== Application Settings ====================
# Default LLM Provider (openai, groq, gemini)
DEFAULT_LLM_PROVIDER = os.getenv("DEFAULT_LLM_PROVIDER", "groq")

# Max tokens for response
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1000"))

# Temperature (0.0 - 1.0, higher = more creative)
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

# Response modes
RESPONSE_MODES = {
    "concise": {
        "description": "Short, summarized replies",
        "system_prompt": "Provide concise, brief answers. Keep responses under 200 words when possible."
    },
    "detailed": {
        "description": "Expanded, in-depth responses",
        "system_prompt": "Provide detailed, comprehensive answers with explanations and examples."
    }
}

# Default response mode
DEFAULT_RESPONSE_MODE = os.getenv("DEFAULT_RESPONSE_MODE", "detailed")

# ==================== Logging Configuration ====================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "./logs/app.log")

# Enable/disable features
ENABLE_RAG = os.getenv("ENABLE_RAG", "true").lower() == "true"
ENABLE_WEB_SEARCH = os.getenv("ENABLE_WEB_SEARCH", "true").lower() == "true"

# ==================== RAG Settings ====================
# Number of documents to retrieve
TOP_K_DOCUMENTS = int(os.getenv("TOP_K_DOCUMENTS", "3"))

# Similarity threshold for document retrieval
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.5"))
