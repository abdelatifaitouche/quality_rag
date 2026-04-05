from fastapi import APIRouter, Depends
from .usecases import GeminiRetrievalUC
from src.features.retrieval.schemas.chat_schemas import ChatRequest, ChatResponse

router = APIRouter(prefix="/retrieval")


def get_service():
    return GeminiRetrievalUC()


@router.post("/chat", response_model=ChatResponse)
def chat(data: ChatRequest, service: GeminiRetrievalUC = Depends(get_service)):
    """
    JUST A SIMPLE QA WITH GEMINI FOR NOW, no rag
    NOTHING, testing purpose
    """
    return service.chat(data)
