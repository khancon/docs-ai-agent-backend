import requests
from bs4 import BeautifulSoup
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from app.config import SITEMAP_URL, MAX_PAGES, CHROMA_DB_DIR, EMBED_MODEL

def get_kubernetes_doc_urls():
    resp = requests.get(SITEMAP_URL)
    soup = BeautifulSoup(resp.text, "xml")
    urls = [loc.text for loc in soup.find_all("loc") if "/docs/" in loc.text]
    return urls[:MAX_PAGES]

def ingest_kubernetes_docs():
    urls = get_kubernetes_doc_urls()
    all_docs = []
    for i, url in enumerate(urls):
        try:
            loader = WebBaseLoader(url)
            docs = loader.load()
            all_docs.extend(docs)
        except Exception as e:
            print(f"Failed to load {url}: {e}")
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(all_docs)

    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    vectorstore = Chroma.from_documents(chunks, embedding=embeddings, persist_directory=CHROMA_DB_DIR)
    return vectorstore
