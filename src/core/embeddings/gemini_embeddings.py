from src.core.embeddings.base import EmbeddingProvider
from src.core.llm.gemini import get_gemini_client
from google.genai import types


class GeminiEmbeddingProvider(EmbeddingProvider):
    def __init__(self):
        self.client = get_gemini_client()

    def batch_embed(self, data: list[str]) -> list[list[float]]:
        BATCH_SIZE: int = 50

        if not data:
            return []

        embeddings: list[list[float]] = []

        for i in range(0, len(data), BATCH_SIZE):
            print(f"BATCH<{i}>: PROCESSING")

            batch = data[i : i + BATCH_SIZE]

            batch_result = self.client.models.embed_content(
                model="gemini-embedding-001",
                contents=batch,  # Runtime ok,
                config=types.EmbedContentConfig(task_type="SEMANTIC_SIMILARITY"),
            )

            if batch_result is None or not getattr(batch_result, "embeddings", None):
                raise RuntimeError("Embedding Failed")

            vectors = [e.values for e in batch_result.embeddings if e and e.values]

            if len(vectors) != len(batch):
                raise RuntimeError("Embedding mismatch")

            embeddings.extend(vectors)
        return embeddings
