from abc import ABC, abstractmethod


class AbstractVectorRepository(ABC):
    @abstractmethod
    def create_collection(self, name: str) -> None:
        pass

    @abstractmethod
    def retrieve(self, collection_name: str, query: str, n_results: int = 2):
        pass
