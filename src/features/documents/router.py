from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from src.features.documents.usecases import DocumentUC
from src.features.documents.schemas.document_schemas import DocumentDetails
from src.api.dependencies.db import get_db
from src.core.common.pagination import Pagination
from src.features.documents.schemas.filters import Filters


router = APIRouter(prefix="/documents")


def get_service(db: AsyncSession = Depends(get_db)):
    return DocumentUC(db)


@router.get("", response_model=list[DocumentDetails])
async def list_documents(
    filters: Filters = Depends(),
    pagination: Pagination = Depends(),
    service: DocumentUC = Depends(get_service),
):
    documents: list[DocumentDetails] = await service.list(filters, pagination)

    return documents


@router.get("/{document_id}", response_model=DocumentDetails)
async def get_document(document_id: str, service: DocumentUC = Depends(get_service)):
    document = await service.get_by_id(UUID(document_id))
    return document
