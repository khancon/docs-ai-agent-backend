# app/rag_pipeline.py

from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from app.config import CHROMA_DB_DIR, EMBED_MODEL, LLM_MODEL, LLM_SERVER

def get_rag_chain():
    # Load the same embedding model used during ingestion
    embedding_function = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

    # Reload vector store with embeddings for querying
    vectorstore = Chroma(
        persist_directory=CHROMA_DB_DIR,
        embedding_function=embedding_function
    )

    # Set up retriever and LLM
    retriever = vectorstore.as_retriever()
    llm = Ollama(model=LLM_MODEL)

    # Build retrieval-augmented QA chain
    rag_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return rag_chain
