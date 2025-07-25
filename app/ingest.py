# app/ingest.py

import os
from app.config import CHROMA_DB_DIR
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from app.config import SITEMAP_URL, MAX_PAGES, EMBED_MODEL
from bs4 import BeautifulSoup
import logging
import requests, time

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, 
    format='%(levelname)-8s %(message)s'
)

def get_doc_urls(sitemap_url=SITEMAP_URL):
    resp = requests.get(sitemap_url)
    logger.info(f"Sitemap status: {resp.status_code}")
    logger.info(f"Content-Type: {resp.headers.get('Content-Type')}")
    # logger.info(resp.text[:500])  # Print a snippet of the response

    soup = BeautifulSoup(resp.text, "xml")
    urls = [loc.text for loc in soup.find_all("loc") if "/docs/" in loc.text]
    for i in range(MAX_PAGES):
        logger.info(f"\tURL {i}: {urls[i]}")
    return urls[:MAX_PAGES]

def ingest_docs(sitemap_url=SITEMAP_URL):
    # if os.path.exists(os.path.join(CHROMA_DB_DIR, "index")):
    #     logger.info("Chroma vectorstore already exists.")
    #     return 0, 0.0
    
    start_time = time.time()

    logger.info("Building Chroma vectorstore from scratch...")
    urls = get_doc_urls(sitemap_url)
    logger.info(f"Found {len(urls)} doc URLs")
    all_docs = []
    total_chars = 0

    for i, url in enumerate(urls):
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            if "text" not in resp.headers.get("Content-Type", ""):
                raise ValueError(f"Non-text content at {url}")
            loader = WebBaseLoader(url)
            docs = loader.load()

            if docs:  # ✅ Only extend if not empty
                all_docs.extend(docs)
                total_chars += sum(len(doc.page_content) for doc in docs)  # 🧠 accumulate size
        except Exception as e:
            logger.info(f"Failed to load {url}: {e}")
    
    logger.info(f"Loaded {len(all_docs)} documents")


    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(all_docs)

    # logger.info(f"\nSample chunk:\n {chunks[0].page_content[:500]}")

    if not chunks:
        raise ValueError("No documents to index. Check if the URLs were loaded and split correctly.")

    logger.info(f"Split into {len(chunks)} chunks")

    # ✅ DEBUG: Write chunks to a file
    # logger.info("Writing debug chunks to 'debug_chunks.txt'...")
    # with open("debug_chunks.txt", "w", encoding="utf-8") as f:
    #     for i, chunk in enumerate(chunks):
    #         logger.info(f"Writing chunk {i+1} with size {len(chunk.page_content)}")
    #         f.write(f"\n--- Chunk #{i+1} ---\n")
    #         f.write(chunk.page_content.strip() + "\n")

    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DB_DIR
    )
    # db.persist()

    elapsed = time.time() - start_time
    logger.info("Chroma vectorstore saved to disk.")

    return total_chars, elapsed
