# app/config.py
import os

# URL of Kubernetes sitemap to crawl
SITEMAP_URL = "https://kubernetes.io/en/sitemap.xml"

# Maximum number of pages to process (helps during testing)
MAX_PAGES = 5

# Directory to store Chroma vector DB
CHROMA_DB_DIR = "/app/chroma_db"

# Embedding model name (HuggingFace model)
EMBED_MODEL = "BAAI/bge-small-en-v1.5"

# Ollama model name (must be pulled locally)
LLM_MODEL = os.getenv("LLM_MODEL", "deepseek-llm")
LLM_SERVER = os.getenv("LLM_SERVER", "http://localhost:11434")
  
OLLAMA_API_URL = "http://ollama:11434"

# Chunking parameters
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
