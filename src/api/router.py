from fastapi import APIRouter
from src.features.retrieval.router import router as retrieval_api
from src.features.ingestion.router import router as ingestion_api
from src.features.documents.router import router as document_api


api_router = APIRouter(prefix="/api/v1")

api_router.include_router(retrieval_api)
api_router.include_router(ingestion_api)
api_router.include_router(document_api)
