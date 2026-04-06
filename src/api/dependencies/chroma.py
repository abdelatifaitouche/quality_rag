from src.core.db.chroma import get_chroma_client


def get_chroma():
    return get_chroma_client()
