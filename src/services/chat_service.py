from src.repositories.interface import AbstractVectorRepository


class ChatService:
    def __init__(self, repo: AbstractVectorRepository):
        self.__repo = repo

    def chat(self, query: str):
        self.query_context(query)
        return

    def query_context(self, query: str):
        data = self.__repo.retrieve()
