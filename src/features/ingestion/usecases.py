from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile
from src.features.documents.repository import DocumentRepository
from src.features.documents.models import Document
from src.features.documents.schemas.document_schemas import (
    DocumentCreate,
    DocumentDetails,
)
from src.features.documents.enums import DocumentStatus


from src.workers.ingestion import ingest_pdf

import aiofiles
import os


class IngestionUC:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db
        self.doc_repo: DocumentRepository = DocumentRepository()

    async def ingest(self, file: UploadFile):
        """
        WRITE THE FILE TO DISK IN ASYNC NON BLOCKING IO
        """

        upload_dir = os.getenv("UPLOAD_DIR", "/app/uploads")
        file_path = f"{upload_dir}/{file.filename}"

        async with aiofiles.open(file_path, "wb") as f:
            total_size: int = 0
            while chunk := await file.read(1024 * 1024):
                total_size += len(chunk)
                await f.write(chunk)

        document: Document = await self.doc_repo.create(
            DocumentCreate(
                name=str(file.filename),
                file_path=file_path,
                file_size=total_size,
                mime_type="pdf",
            ),
            self.db,
        )

        await self.db.commit()

        task = ingest_pdf.delay(document.id, file_path)

        return {"document_id": document.id, "status": document.status}
