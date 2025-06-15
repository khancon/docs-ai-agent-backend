from fastapi import APIRouter
from pydantic import BaseModel
from app.rag_pipeline import get_rag_chain

router = APIRouter()
rag_chain = get_rag_chain()

class Query(BaseModel):
    query: str

@router.post("/chat")
async def chat(query: Query):
    # New: Use .invoke() instead of .run()
    result = rag_chain.invoke({"query": query.query})
    return {"answer": result}