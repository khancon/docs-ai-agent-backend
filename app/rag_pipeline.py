# app/rag_pipeline.py

from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM

from langchain.chains import RetrievalQA
from app.config import CHROMA_DB_DIR, EMBED_MODEL, LLM_SERVER
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, 
    format='%(levelname)-8s %(message)s'
)
def get_rag_chain(model_name: str):
    # Load the same embedding model used during ingestion
    embedding_function = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

    # Reload vector store with embeddings for querying
    vectorstore = Chroma(
        persist_directory=CHROMA_DB_DIR,
        embedding_function=embedding_function
    )

    # Set up retriever and LLM
    retriever = vectorstore.as_retriever()

    # DEBUG: Print retrieved chunks for a test query
    docs = retriever.get_relevant_documents("What is APIServiceSpec?")
    for i, doc in enumerate(docs):
        logger.info(f"\n--- Chunk {i+1} ---\n{doc.page_content[:300]}")

    llm = OllamaLLM(
        model=model_name,
        base_url=LLM_SERVER
    )

    # Build retrieval-augmented QA chain
    rag_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return rag_chain
