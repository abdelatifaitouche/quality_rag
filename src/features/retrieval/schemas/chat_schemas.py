from pydantic import BaseModel


class ChatRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
    response: str | None = None

    model_config = {"from_attributes": True}
