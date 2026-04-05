from langchain_core.documents import Document
import unicodedata
import re


class TextProcessor:
    """
    Text Processor will clean the pdf from noise,

    Normilize the texts

    checks for empty pages

    returns a cleaned version of the text inside the pds
    """

    def process(self, docs: list[Document]) -> list[Document]:
        cleaned_docs: list[Document] = []

        for doc in docs:
            text = doc.page_content
            text = self._text_normalization(text)
            text = self._clean_text(text)

            if len(text.strip()) > 50:
                doc.page_content = text
                doc.metadata.update(
                    {
                        "length": len(text),
                        "source": doc.metadata.get("source", "unknown"),
                    }
                )
                cleaned_docs.append(doc)

        return cleaned_docs

    def _text_normalization(self, text: str):
        text = unicodedata.normalize("NFKC", text)
        text = text.replace("\x95", "•").replace("\x96", "-")
        text = text.replace("\u2018", "'").replace("\u2019", "'")
        text = text.replace("\u201c", '"').replace("\u201d", '"')
        return text

    def _clean_text(self, text: str) -> str:
        text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)
        text = re.sub(r" {2,}", " ", text)
        text = re.sub(r"[^\x20-\x7E\n]", " ", text)
        return text.strip()
