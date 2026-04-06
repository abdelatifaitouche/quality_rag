from langchain_core.documents import Document
from .text_processor import TextProcessor
from pathlib import Path
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import hashlib


class Chunker:
    """
    Ingestion Pipeline is an orchestrator for the whole process of loading the pdfs from a file,

    pass it to a text cleaning process,

    then split the documents into chunks using for now the RecursiveCharacterSplitter (needs to search for semantic and hybrid types)

    generate ids for each chunks using the md5 to avoid duplicates and sequentials ids

    returns the chunks to get feed into the vector database


    For now this is basic, needs to seperate chunking into its own class to handle it better
    and to keep this pipeline modular
    """

    def __init__(self, text_processor: TextProcessor):
        self.text_processor: TextProcessor = text_processor

    def chunk(self, file_path: Path):
        """ENTRY POINT"""

        if not file_path.exists():
            raise FileNotFoundError(f"File Not Found at {file_path}")

        loader = PyMuPDFLoader(file_path=str(file_path))

        docs = loader.load()

        cleaned_docs_text = self.text_processor.process(docs)

        chunks = self.chunking(cleaned_docs_text)

        return chunks

    def generate_chunk_id(self, text, source, page) -> str:
        raw = f"{source}_{page}_{text[100:]}"
        return hashlib.md5(raw.encode()).hexdigest()

    def chunking(self, docs: list[Document]):
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
