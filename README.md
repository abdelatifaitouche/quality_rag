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
 - the simple rag Q&A is working but thats not enough
 - i need next to : 
    - test reranking
    - hybrid search : bm25 + similarity search
    - better chunking
    - add ingestion job SQL model to track the ingestion pipeline jobs
    - add DocumentChunk SQL Model to have a vision on how the chunking is and how to improve
    - add QueryLog SQL MODEL to track query logs and how the model perform
    - also work on the main feature : document review 

  - for the document review feature : 
    i guess, am going to create a temp collection for each document uploaded by the employee
    do a similarity comparaision or search maybe between the main collection (quality stds) and the employee collection
    return a pydantic score based on some criteria 
