from enum import StrEnum


class DocumentStatus(StrEnum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    INGESTED = "INGESTED"
    ARCHIVED = "ARCHIVED"
    FAILED = "FAILED"
