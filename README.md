# 🧠 Kubernetes Docs AI Chatbot (RAG + DeepSeek-V3)

This project is a fully local, retrieval-augmented chatbot that can answer questions about the entire [Kubernetes documentation](https://kubernetes.io/docs/) using the power of open-source LLMs.

It uses:
- 🧾 Sitemap crawling to ingest all Kubernetes docs
- ✂️ Chunking + embedding with `bge-small-en-v1.5`
- 🧠 Fast local inference with `DeepSeek-V3` via Ollama
- 💬 Conversational interface in the command line

---

## 🚀 How It Works

1. Fetches up to `MAX_PAGES` doc pages from `https://kubernetes.io/sitemap.xml`
2. Extracts and splits page content into chunks
3. Embeds chunks with a sentence-transformer model
4. Stores them in a local Chroma vector DB
5. When you ask a question:
   - It retrieves the most relevant chunks
   - Sends them along with your query to DeepSeek-V3
   - Returns a grounded, helpful answer

---

## 📦 Requirements

- Python 3.10+
- Ollama (for running `deepseek-llm`)
- pip packages:

```bash
pip install langchain langchain-community chromadb sentence-transformers bs4 requests
```

---

## 🧠 LLM Setup (DeepSeek-V3)

Make sure Ollama is installed and running:

```bash
# Install and start the LLM
ollama pull deepseek-llm
ollama run deepseek-llm
```

---

## 💬 Usage

```bash
python rag_agent_deepseek_v3.py
```

Then start chatting:

```
You: What is a Pod in Kubernetes?
Bot: A Pod is the smallest deployable unit in Kubernetes...
```

---

## 🧰 Configuration

- `MAX_PAGES`: How many doc pages to scrape (for testing)
- `CHROMA_DB_DIR`: Where to store vector DB
- `LLM_MODEL`: Ollama model name (default: `deepseek-llm`)
- `EMBED_MODEL`: HuggingFace embedding model (default: `bge-small-en-v1.5`)

---

## 📌 Roadmap

- [ ] Turn into FastAPI backend
- [ ] Add a React or Next.js frontend
- [ ] Multi-source config support
- [ ] Deploy with Docker Compose

---

## 📜 License

MIT
