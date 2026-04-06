from fastapi import APIRouter, Depends, UploadFile, File
from src.api.dependencies.db import get_db
from src.features.ingestion.usecases import IngestionUC
from src.api.dependencies.chroma import get_chroma
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/ingestion")


def get_uc(db: AsyncSession = Depends(get_db)):
    return IngestionUC(db)


@router.post("/ingest")
async def ingest(data: UploadFile = File(...), service: IngestionUC = Depends(get_uc)):
    return await service.ingest(data)
