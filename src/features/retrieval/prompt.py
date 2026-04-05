from src.features.retrieval.schemas.base_prompt import PromptTemplate


"""
    Use this file to test and configure multiple types of 
    prompts,

    using the PromptTemplate Dataclass with $query placeholder
"""


DEFAULT_PROMPT = PromptTemplate(
    system="""You are an expert quality consultant at a Big Four firm.Be concise, structured""",
    user=""" QUERY : $query """,
)
