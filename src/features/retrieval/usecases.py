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

load_dotenv()


class GeminiRetrievalUC(IRetrievalUC):
    def __init__(self, prompt: PromptTemplate = DEFAULT_PROMPT):
        self.model: str = "gemini-3-flash-preview"
        self.client = genai.Client(api_key=os.getenv("API_KEY"))
        self._prompt = prompt

    def chat(self, query: ChatRequest) -> ChatResponse:
        """
        THIS IS THE CURRENT RETRIEVAL METHOD,
        it works for now,

        not much work, but honest work
        """
        client = get_chroma_client()

        collection = client.get_or_create_collection(name="quality_test")

        results = collection.query(query_texts=[query.query], n_results=4)

        docs = results["documents"][0]

        context_text = "\n\n---\n\n".join(docs)

        user_message = self._prompt.render(query.query, context_text)

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
