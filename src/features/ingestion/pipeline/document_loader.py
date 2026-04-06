from pathlib import Path
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document


class DocumentLoader:
    """
    Document Loader class to handle loading the pdfs from the disk
    using now PyMuPDFLoader, may switch
    """

    def load(self, file_path: Path) -> list[Document]:
        if not file_path.exists():
            raise FileNotFoundError(f"File not Found at {file_path}")

        loader = PyMuPDFLoader(file_path=file_path)

        docs: list[Document] = loader.load()

        return docs
