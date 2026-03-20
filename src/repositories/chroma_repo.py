from src.repositories.interface import AbstractVectorRepository


class ChromaRepository(AbstractVectorRepository):
    def __init__(self):
        pass

    def create_collection(self, name: str):
        return

    def retrieve(self, collection_name: str, query: str, n_results: int = 2):
        return
