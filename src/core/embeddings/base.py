from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):
    """
    Embedding Provider Interface,
    """

    def batch_embed(self, data: list[str]) -> list[list[float]]:
        """Batch Processing for embedding"""
        raise NotImplementedError
