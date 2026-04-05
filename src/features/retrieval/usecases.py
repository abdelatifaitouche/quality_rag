from google import genai
from google.genai import types
from .uc_interface import IRetrievalUC
from dotenv import load_dotenv
import os

from src.features.retrieval.schemas.base_prompt import PromptTemplate
from src.features.retrieval.prompt import DEFAULT_PROMPT
from typing import cast, Sequence
from src.features.retrieval.schemas.chat_schemas import ChatResponse, ChatRequest

load_dotenv()


class GeminiRetrievalUC(IRetrievalUC):
    def __init__(self, prompt: PromptTemplate = DEFAULT_PROMPT):
        self.model: str = "gemini-3-flash-preview"
        self.client = genai.Client(api_key=os.getenv("API_KEY"))
        self._prompt = prompt

    def chat(self, query: ChatRequest) -> ChatResponse:
        user_message = self._prompt.render(query.query)

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
