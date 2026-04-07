from pydantic import BaseModel


class Pagination(BaseModel):
    page: int = 1
    limit: int = 10

    @property
    def offset(self):
        return (self.page - 1) * self.limit
