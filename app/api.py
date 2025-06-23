from fastapi import APIRouter
from pydantic import BaseModel
from app.rag_pipeline import get_rag_chain
import requests
from app.config import LLM_SERVER
from app.ollama_utils import pull_model, is_model_available
from fastapi import HTTPException

router = APIRouter()

class Query(BaseModel):
    query: str
    model_name: str

@router.post("/chat")
async def chat(query: Query):
    # Check if model is available
    if not is_model_available(query.model_name):
        pull_model(query.model_name)

    # Build the RAG chain using the requested model
    rag_chain = get_rag_chain(query.model_name)
    result = rag_chain.invoke({"query": f"Answer concisely without inner thoughts. Do not include thinking steps or commentary. {query.query}"})
    return {"answer": result}

@router.get("/models")
async def list_models():
    try:
        resp = requests.get(f"{LLM_SERVER}/api/tags")
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e)}

@router.delete("/models/{model_name}")
async def delete_model(model_name: str):
    try:
        resp = requests.delete(f"{LLM_SERVER}/api/delete", json={"name": model_name})
        resp.raise_for_status()
        return {"message": f"Model '{model_name}' deleted successfully."}
    except Exception as e:
        return {"error": str(e)}
    
class ModelRequest(BaseModel):
    model_name: str

@router.post("/models/pull")
async def pull_model_endpoint(model_request: ModelRequest):
    try:
        result = pull_model(model_request.model_name)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))