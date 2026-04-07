from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.sql import Select
from uuid import UUID

from src.features.documents.models import Document
from src.features.documents.schemas.document_schemas import DocumentCreate
from src.core.common.pagination import Pagination
from src.features.documents.schemas.filters import Filters


class DocumentRepository:
    async def create(self, data: DocumentCreate, db: AsyncSession) -> Document:
        doc: Document = Document(**data.model_dump())
        db.add(doc)
        await db.flush()
        return doc

    async def get_by_id(self, document_id: UUID, db: AsyncSession) -> Document | None:
        stmt = select(Document).where(Document.id == document_id)

        result = await db.execute(stmt)

        return result.scalars().one_or_none()

    def apply_filters(self, stmt, filters: Filters):
        if filters.status:
            stmt = stmt.where(Document.status == filters.status)

        return stmt

    async def list(
        self, filters: Filters | None, pagination: Pagination, db: AsyncSession
    ) -> list[Document]:
        stmt = select(Document)

        if filters:
            stmt = self.apply_filters(stmt, filters)

        stmt = (
            stmt.offset(pagination.offset)
            .limit(pagination.limit)
            .order_by(Document.created_at)
        )

        results = await db.execute(stmt)

        return list(results.scalars().all())

    async def update(self):
        return

    async def delete(self):
        return
