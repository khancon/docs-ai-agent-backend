from fastapi import FastAPI
from app.api import router
from app.ingest import ingest_kubernetes_docs
from contextlib import asynccontextmanager
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, 
    format='%(levelname)-8s %(message)s'
)
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up and ingesting docs if needed...")
    total_size, duration = ingest_kubernetes_docs()
    if total_size > 0:
        logger.info(f"Ingested {total_size:,} characters of documentation in {duration:.2f} seconds.")
    else:
        logger.info("Ingestion skipped (vectorstore already exists).")

    yield  # 👈 This is where FastAPI continues with normal startup

app = FastAPI(title="K8s Docs Chatbot API", lifespan=lifespan)

app.include_router(router)

    # Optional: do any cleanup here after shutdown

# app = FastAPI(title="K8s Docs Chatbot API")

# def startup_event():
#     logger.info("Starting up and ingesting docs if needed...")
#     total_size, duration = ingest_kubernetes_docs()
#     if total_size > 0:
#         logger.info(f"Ingested {total_size:,} characters of documentation in {duration:.2f} seconds.")
#     else:
#         logger.info("Ingestion skipped (vectorstore already exists).")

# app.include_router(router)
