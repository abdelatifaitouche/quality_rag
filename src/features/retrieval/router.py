from fastapi import APIRouter


router = APIRouter(prefix="/retrieval")


@router.get("")
def home():
    return "retreival"
