from sqlalchemy.orm import Mapped, mapped_column
from src.core.db.base import Base
from src.features.documents.enums import DocumentStatus
from sqlalchemy import String, Integer, Enum, Text


class Document(Base):
    __tablename__ = "documents"

    name: Mapped[str] = mapped_column(String, nullable=False)
    file_path: Mapped[str] = mapped_column(String, nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)
    mime_type: Mapped[str] = mapped_column(String, nullable=False)

    status: Mapped[DocumentStatus] = mapped_column(
        Enum(DocumentStatus),
        default=DocumentStatus.PENDING,
        nullable=False,
    )
