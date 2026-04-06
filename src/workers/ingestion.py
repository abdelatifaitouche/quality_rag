from src.workers.celery_app import celery_app


@celery_app.task(bind=True, name="ingest_pdf")
def ingest_pdf(self, document_id: str, file_path: str):
    import asyncio

    async def run():
        from pathlib import Path
        from src.core.db.session import AsyncSessionLocal
        from src.features.documents.models import Document
        from src.features.documents.enums import DocumentStatus

        from src.features.ingestion.pipeline.document_loader import DocumentLoader
        from src.features.ingestion.pipeline.text_processor import TextProcessor
        from src.features.ingestion.pipeline.chunker import Chunker
        from src.features.ingestion.pipeline.ingestion_pipeline import IngestionPipeline

        from src.core.db.chroma import get_chroma_client

        async with AsyncSessionLocal() as db:
            document: Document | None = await db.get(Document, document_id)
            if not document:
                return

            document.status = DocumentStatus.PROCESSING
            await db.commit()

            loader = DocumentLoader()
            processor = TextProcessor()
            chunker = Chunker()
            vector_store = get_chroma_client()
            pipeline = IngestionPipeline(
                loader,
                chunker,
                processor,
                vector_store,
            )

            pipeline.run(Path(file_path), "quality_test")

            document.status = DocumentStatus.INGESTED
            await db.commit()

    try:
        asyncio.run(run())
    except Exception as e:
        raise e
