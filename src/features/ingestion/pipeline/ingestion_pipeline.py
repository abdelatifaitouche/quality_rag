from pathlib import Path
from .document_loader import DocumentLoader
from .chunker import Chunker
from .text_processor import TextProcessor

from langchain_core.documents import Document


class IngestionPipeline:
    def __init__(self, loader, chunker, processor, vector_store):
        self.loader: DocumentLoader = loader
        self.processor: TextProcessor = processor
        self.chunker: Chunker = chunker
        self.vector_store = vector_store

    def run(self, file_path: Path, collection: str):
        print("Starting the Ingestion Pipeline")
        print(f"Loading the doc at {file_path}")
        docs: list[Document] = self.loader.load(file_path)

        print(f"Text cleaning for {len(docs)} Document")
        cleaned_texts: list[Document] = self.processor.process(docs)

        print("Chunking the Cleaned Documents")
        chunks: list[Document] = self.chunker.chunk(cleaned_texts)

        print(f"Total Chunks {len(chunks)}")
        collection_db = self.vector_store.get_or_create_collection(name=collection)

        print("Inserting into the Vector Database .............")
        collection_db.upsert(
            documents=[d.page_content for d in chunks],
            ids=[d.metadata["chunk_id"] for d in chunks],
            metadatas=[d.metadata for d in chunks],
        )

        print("Pipeline Finished")
