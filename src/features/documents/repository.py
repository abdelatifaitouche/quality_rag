from sqlalchemy.ext.asyncio import AsyncSession

from src.features.documents.models import Document
from src.features.documents.schemas import DocumentCreate


class DocumentRepository:
    async def create(self, data: DocumentCreate, db: AsyncSession) -> Document:
        doc: Document = Document(**data.model_dump())
        db.add(doc)
        await db.flush()
        return doc

    async def list(self):
        return

    async def update(self):
        return

    async def delete(self):
        return
