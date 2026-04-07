from src.core.common.base_filters import BaseFilters
from src.features.documents.enums import DocumentStatus


class Filters(BaseFilters):
    status: DocumentStatus | None = None
