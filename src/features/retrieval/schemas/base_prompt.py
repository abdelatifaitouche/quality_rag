from dataclasses import dataclass
from string import Template


@dataclass
class PromptTemplate:
    system: str
    user: str

    def render(self, query: str, context: str) -> str:
        return Template(self.user).substitute(query=query, context=context)
