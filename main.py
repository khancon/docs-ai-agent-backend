from fastapi import FastAPI
from app.api import router

app = FastAPI(title="K8s Docs Chatbot API")
app.include_router(router)
