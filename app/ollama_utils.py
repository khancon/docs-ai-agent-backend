import requests
from app.config import OLLAMA_API_URL
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, 
    format='%(levelname)-8s %(message)s'
)

def is_model_available(model_name: str) -> bool:
    response = requests.get(f"{OLLAMA_API_URL}/api/tags")
    if response.status_code != 200:
        return False
    tags = response.json().get("models", [])
    return any(tag["name"] == model_name for tag in tags)

def pull_model(model_name: str) -> dict:
    if is_model_available(model_name):
        return {"status": "already_available", "model": model_name}
    
    response = requests.post(f"{OLLAMA_API_URL}/api/pull", json={"name": model_name})
    if response.status_code != 200:
        raise Exception(f"Failed to pull model: {response.text}")
    
    return {"status": "pulled", "model": model_name}
