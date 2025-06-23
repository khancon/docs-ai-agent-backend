# 🧠 Docs AI Chatbot Backend (RAG + Ollama)

This is the **backend** for a Kubernetes documentation chatbot that uses Retrieval-Augmented Generation (RAG) with a local open-source LLM. The system provides accurate, grounded answers to technical questions by querying embedded chunks of the official [Kubernetes documentation](https://kubernetes.io/docs/).

---

## 🔧 Features

- 🧭 **Documentation Ingestion**: Crawls the official Kubernetes docs via the sitemap and extracts page content.
- ✂️ **Text Chunking**: Splits long documents into smaller, overlapping chunks using LangChain’s `RecursiveCharacterTextSplitter`.
- 🧠 **Embeddings**: Converts text chunks into embeddings using `bge-small-en-v1.5` via HuggingFace, storing them in a persistent Chroma vector database.
- 🧾 **RAG Pipeline**: Uses a combination of retriever and LLM (DeepSeek-R1 via Ollama) to generate grounded responses.
- 🚀 **FastAPI Server**: Exposes a `/chat` endpoint for querying the system with a user question and receiving a synthesized answer.
- 🐳 **Containerized**: Fully containerized using Docker and `docker-compose`, allowing for reproducible local development.

---

## 📦 Setup Instructions

### 1. Clone and Set Up Python Virtual Environment

```bash
git clone https://github.com/your-username/docs-ai-agent.git
cd docs-ai-agent

# Create a virtual environment and activate it
python -m venv venv
source venv/bin/activate

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 2. Run with Docker Compose

Use the Makefile command below to clean and rebuild your Docker containers:

```bash
make clean-docker-rebuild
```

This will:
- Stop and remove any previous containers and volumes.
- Rebuild the FastAPI backend and Ollama containers.
- Launch the entire application stack locally.

Ensure Ollama is installed on your system for the model to run inside the container.

---

## 💬 API Endpoints

### POST `/chat`

Submits a user query to the backend and receives a response grounded in the Kubernetes docs.

**Request Example:**

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is a Kubernetes Pod?", "model_name": "deepseek-r1:1.5b"}'
```

**Response Format:**

```json
{
  "answer": {
    "query": "What is a Kubernetes Pod?",
    "result": "A Kubernetes Pod is the smallest deployable unit that can be created and managed in Kubernetes..."
  }
}
```

---

### GET `/models`

Returns a list of models currently available to the Ollama server.

```bash
curl http://localhost:8000/models
```

---

### POST `/models/pull`

Downloads and installs a new LLM to the local Ollama instance.

```bash
curl -X POST http://localhost:8000/models/pull \
  -H "Content-Type: application/json" \
  -d '{"model_name": "deepseek-r1:1.5b"}'
```

---

## 📁 Project Structure

```text
docs-ai-agent/
├── app/
│   ├── api.py              # Defines all FastAPI routes
│   ├── rag_pipeline.py     # RAG logic and LLM + retriever setup
│   ├── ingest.py           # Web crawler and embedding pipeline
│   ├── ollama_utils.py     # Utility functions for managing Ollama models
│   └── config.py           # Configuration settings and constants
├── chroma_db/              # Local persistent Chroma vector database
├── Dockerfile              # FastAPI app Docker image
├── Dockerfile.ollama       # Ollama server Docker image
├── docker-compose.yml      # Orchestration config for Docker containers
├── Makefile                # Handy dev commands (build, run, clean, etc.)
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## 🧠 How It Works

1. **Ingestion**: The `ingest.py` script downloads and parses documentation pages using their sitemap, chunks content, and generates vector embeddings.
2. **Storage**: The Chroma vector database stores these embeddings locally for efficient semantic retrieval.
3. **Querying**: When a user sends a question to `/chat`, the app:
   - Converts the query into an embedding
   - Finds the most relevant document chunks
   - Passes them as context to the LLM using a prompt template
4. **Answer Generation**: The LLM (e.g., DeepSeek-R1) returns a final response based on the context and question.

---

## 🧩 Related Projects

- 🔗 [Frontend Chat UI](https://github.com/your-username/docs-ai-agent-frontend) *(Coming soon)*

---

## 📜 License

MIT
