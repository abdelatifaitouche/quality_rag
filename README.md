# Quality Reviewer Assistant

The main Idea right now is for users to be able to upload their final work (pptx, pdfs)
the system will review the work against the set of guidelines and recommandations of the global firm Quality Standards


## How it works ????

idk yet but this is what i came up with :

User Uploads a document

Document Parsing using Docling + Chunking

Chromadb Stores and retreives what needed

Gemini Evaluates the query and returns a structured response (using pydantic)


### stack : 


Fastapi
Chromadb for now (will swap and test later other techs)
Gemini for now (since its free to use)


