from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from app.config import CHROMA_DB_DIR, LLM_MODEL

def get_rag_chain():
    vectorstore = Chroma(persist_directory=CHROMA_DB_DIR, embedding_function=None)  # uses stored embeddings
    retriever = vectorstore.as_retriever()
    llm = Ollama(model=LLM_MODEL)
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
