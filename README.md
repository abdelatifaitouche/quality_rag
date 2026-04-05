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

### WHAT I DID TIL NOW : 

- Changed the project structure to feature based : 
    - features 
        - ingestion feature
        - retrieval feature
        - document management feature 

- implemented a simple ingestion pipeline, no embedding nothing
just text processing , chunking thats it

- tested the gemini api call with a simple request 

- since i might switch to claude later, am opting for a strategy pattern in the UC, created a UC interface, that the Gemini or Claude 
will use, 

- Prompt : Instead of hardcoding the prompt, i created a PromptTemplate, with a DEFAULT_PROMPT, this way i can inject it direclty and 
test multiple styles!!!!
