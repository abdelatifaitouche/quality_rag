from pathlib import Path
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import re
import unicodedata
from langchain_core.documents import Document
import hashlib

BASE_DIR = Path(__file__).parent.parent

PDF_PATH = BASE_DIR / "data" / "quality_doc.pdf"


class TextProcessor:
    """
    Text Processor will clean the pdf from noise,

    Normilize the texts

    checks for empty pages

    returns a cleaned version of the text inside the pds
    """

    def process(self, docs: list[Document]) -> list[Document]:
        cleaned_docs: list[Document] = []

        for doc in docs:
            text = doc.page_content
            text = self._text_normalization(text)
            text = self._clean_text(text)

            if len(text.strip()) > 50:
                doc.page_content = text
                doc.metadata.update(
                    {
                        "length": len(text),
                        "source": doc.metadata.get("source", "unknown"),
                    }
                )
                cleaned_docs.append(doc)

        return cleaned_docs

    def _text_normalization(self, text: str):
        text = unicodedata.normalize("NFKC", text)
        text = text.replace("\x95", "•").replace("\x96", "-")
        text = text.replace("\u2018", "'").replace("\u2019", "'")
        text = text.replace("\u201c", '"').replace("\u201d", '"')
        return text

    def _clean_text(self, text: str) -> str:
        text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)
        text = re.sub(r" {2,}", " ", text)
        text = re.sub(r"[^\x20-\x7E\n]", " ", text)
        return text.strip()


class IngestionPipeline:
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

    def run(self, file_path: Path):
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
