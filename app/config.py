# app/config.py

# URL of Kubernetes sitemap to crawl
SITEMAP_URL = "https://kubernetes.io/sitemap.xml"

# Maximum number of pages to process (helps during testing)
MAX_PAGES = 100

# Directory to store Chroma vector DB
CHROMA_DB_DIR = "./chroma_db"

# Embedding model name (HuggingFace model)
EMBED_MODEL = "BAAI/bge-small-en-v1.5"

# Ollama model name (must be pulled locally)
LLM_MODEL = "deepseek-llm"
LLM_SERVER = "http://123.45.67.89:11434"  # Replace with actual server IP or domain

# Chunking parameters
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
