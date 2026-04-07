from google import genai
from google.genai import types
from .uc_interface import IRetrievalUC
from dotenv import load_dotenv
import os

from src.features.retrieval.schemas.base_prompt import PromptTemplate
from src.features.retrieval.prompt import DEFAULT_PROMPT
from typing import cast, Sequence
from src.features.retrieval.schemas.chat_schemas import ChatResponse, ChatRequest
from src.core.db.chroma import get_chroma_client
from src.core.llm.gemini import get_gemini_client

load_dotenv()


class GeminiRetrievalUC(IRetrievalUC):
    def __init__(self, prompt: PromptTemplate = DEFAULT_PROMPT):
        self.model: str = "gemini-3-flash-preview"
        self.client = get_gemini_client()
        self._prompt = prompt

    def _retreiver(self, collection_name: str, query: str):
        client = get_chroma_client()

        collection = client.get_or_create_collection(name=collection_name)

        results = collection.query(query_texts=[query], n_results=5)

        return results

    def _context_builder(self, query: str) -> str:
        results = self._retreiver("quality_test", query)

        docs = results.get("documents", [])

        docs = docs[0] if docs else []

        metadatas = results.get("metadatas", [])

        metadatas = metadatas[0] if metadatas else []

        context_chunks = [
            f"{doc}\nSOURCE{meta.get('source')}" for doc, meta in zip(docs, metadatas)
        ]

        context_text = "\n\n---\n\n".join(context_chunks)

        return context_text

    def chat(self, query: ChatRequest) -> ChatResponse:
        """
        THIS IS THE CURRENT RETRIEVAL METHOD,
        it works for now,

        not much work, but honest work
        """

        context: str = self._context_builder(query.query)

        user_message = self._prompt.render(query.query, context)

        contents: list[types.Content] = [
            types.Content(
                role="system", parts=[types.Part.from_text(text=self._prompt.system)]
            ),
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=user_message),
                ],
            ),
        ]

        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,  # type: ignore[arg-type]
        )

        return ChatResponse(response=response.text)
