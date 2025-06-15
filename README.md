# 🧠 Docs AI Chatbot Backend (RAG + DeepSeek-V3)

This is the **backend service** powering a Kubernetes documentation chatbot. It uses a retrieval-augmented generation (RAG) pipeline to answer technical questions grounded in the official [Kubernetes documentation](https://kubernetes.io/docs/), powered entirely by open-source models.

---

## 🔧 What This Backend Does

- 🧾 Crawls the Kubernetes documentation sitemap
- ✂️ Chunks and embeds documentation using `bge-small-en-v1.5`
- 💽 Stores embeddings in a local Chroma vector DB
- 🤖 Serves answers via RAG pipeline using `DeepSeek-V3` running locally via Ollama
- 📡 Exposes a FastAPI endpoint (`/chat`) for integration with a frontend

---

## 📦 Requirements

- Python 3.10+
- Ollama (to run `deepseek-llm` model)
- pip packages:

```bash
pip install -r requirements.txt
```

---

## 🧠 LLM Setup (DeepSeek-V3)

Install and run the DeepSeek LLM using Ollama:

```bash
ollama pull deepseek-llm
ollama run deepseek-llm
```

---

## 💬 API Usage

Start the backend server:

```bash
uvicorn main:app --reload
```

Example `POST` request:

```bash
curl -X POST http://localhost:8000/chat \\
  -H "Content-Type: application/json" \\
  -d '{"query": "What is a Kubernetes Pod?"}'
```

---

## 📁 Project Structure

```
backend/
├── app/
│   ├── api.py            # FastAPI route definitions
│   ├── rag_pipeline.py   # LLM + retriever + RAG setup
│   ├── ingest.py         # Doc crawler, chunking, embedding
│   └── config.py         # Model and storage configuration
├── chroma_db/            # Local vector DB
├── main.py               # FastAPI entrypoint
├── requirements.txt
└── README.md
```

---

## 📌 Roadmap

- [x] Ingest Kubernetes documentation via sitemap
- [x] Generate and store embeddings using Chroma
- [ ] Expose FastAPI `/chat` endpoint
- [ ] Add `/ingest` endpoint for on-demand refresh
- [ ] Add source metadata to answers
- [ ] Containerize with Docker
- [ ] Deploy on Fly.io or Render

---

## 🧩 Related Projects

- 🔗 [Frontend repo (Chat UI)](https://github.com/your-username/docs-ai-agent-frontend) *(Coming soon)*

---

## 📜 License

MIT
