from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

_gemini_client = None


def get_gemini_client():
    global _gemini_client

    if not _gemini_client:
        _gemini_client = genai.Client(api_key=os.getenv("API_KEY"))

        return _gemini_client

    return _gemini_client
