from pydantic import BaseModel
from src.features.documents.enums import DocumentStatus
import uuid


class DocumentCreate(BaseModel):
    name: str
    file_path: str
    status: DocumentStatus = DocumentStatus.PENDING
    file_size: int
    mime_type: str


class DocumentDetails(BaseModel):
    id: uuid.UUID
    name: str
    file_path: str
    status: DocumentStatus
    file_size: int
    mime_type: str
