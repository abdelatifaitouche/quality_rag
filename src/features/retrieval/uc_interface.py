from abc import ABC, abstractmethod
from typing import Any


class IRetrievalUC(ABC):
    @abstractmethod
    def chat(self, query: Any) -> Any:
        """
        QA method :
        args :
            query : a user query string
        return :
            output of the llm selected
        """
        pass
