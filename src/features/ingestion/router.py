from fastapi import APIRouter, Depends, UploadFile
from src.api.dependencies.chroma import get_chroma

router = APIRouter(prefix="/ingestion")


@router.post("/ingest")
def ingest(data=UploadFile, chroma=Depends(get_chroma)):
    return
