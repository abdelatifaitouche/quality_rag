from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID


from src.features.documents.schemas.document_schemas import DocumentDetails
from src.features.documents.repository import DocumentRepository
from src.core.common.pagination import Pagination
from src.features.documents.schemas.filters import Filters


class DocumentUC:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db
        self.repo: DocumentRepository = DocumentRepository()

    async def list(
        self, filters: Filters | None, pagination: Pagination
    ) -> list[DocumentDetails]:
        documents = await self.repo.list(filters, pagination, self.db)

        return [DocumentDetails.model_validate(d) for d in documents]

    async def get_by_id(self, document_id: UUID) -> DocumentDetails:
        doc = await self.repo.get_by_id(document_id, self.db)

        return DocumentDetails.model_validate(doc)

    async def create(self):
        pass

    async def soft_delete(self):
        pass

    async def update(self):
        pass
