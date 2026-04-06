import chromadb
import os


_client = None


def get_chroma_client():
    global _client

    if _client is None:
        _client = chromadb.HttpClient(
            host=os.getenv("CHROMA_HOST", "chromadb"),
            port=int(os.getenv("CHROMA_PORT", 8000)),
        )

    return _client
