from langchain_core.documents import Document
from .text_processor import TextProcessor
from pathlib import Path
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import hashlib


class Chunker:
    def generate_chunk_id(self, text, source, page) -> str:
        raw = f"{source}_{page}_{text[100:]}"
        return hashlib.md5(raw.encode()).hexdigest()

    def chunk(self, docs: list[Document]):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=150,
            separators=["\n\n", "\n", ".", " ", ""],
        )

        chunks: list[Document] = text_splitter.split_documents(docs)

        for i, chunk in enumerate(chunks):
            chunk_id: str = self.generate_chunk_id(
                chunk.page_content, chunk.metadata["source"], chunk.metadata["page"]
            )
            chunk.metadata.update(
                {
                    "chunk_id": chunk_id,
                    "chunk_index": i,
                    "length": len(chunk.page_content),
                }
            )

            chunk.id = chunk_id

        return chunks
