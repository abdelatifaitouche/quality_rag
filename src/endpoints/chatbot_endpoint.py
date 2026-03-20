from fastapi import FastAPI
import chromadb
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from google import genai
from dotenv import load_dotenv


load_dotenv()

gemini_client = genai.Client(api_key=os.getenv("API_KEY"))


class DataPipeLine:
    def __init__(self, collection):
        self.collection = collection

    def run(self):
        print("Start Processing Data")
        docs = self.data_parsing()
        chunks = self.data_chunking(docs)

        data_indexing = self.data_indexing(chunks)
        print("Finished Processing data")

    def data_parsing(self):
        loader = PyPDFLoader("./data/quality_doc.pdf")

        return loader.load_and_split()

    def data_chunking(self, docs):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )

        chunks = text_splitter.split_documents(docs)

        return chunks

    def data_indexing(self, chunks):
        docs = []
        ids = []

        for id, page in enumerate(chunks):
            docs.append(page.page_content)
            ids.append(f"id_{id}")

        self.collection.upsert(documents=docs, ids=ids)


class RagPipeline:
    def __init__(self, db_path: str):
        self.__API_KEY = API_KEY
        self.__db_path = db_path
        self.__db_client = self.get_db_client(db_path)
        self.__collection = self.__db_client.get_or_create_collection(
            name="test_collection", metadata={"hnsw:space": "cosine"}
        )
        self.data_processing = DataPipeLine(self.__collection)

    def get_db_client(self, db_path):
        client = chromadb.PersistentClient(path=db_path)
        return client

    def retrieve(self, query: str):
        collection = self.__collection

        query_results = collection.query(query_texts=query, n_results=2)

        PROMPT = f"You are An expert quality consultant for a big four firm, answer this query : {query}, based on these documents : {query_results}"

        response = gemini_client.models.generate_content(
            model="gemini-3-flash-preview", contents=PROMPT
        )

        return response


chatbot = RagPipeline("./test_db")

print(chatbot.retrieve("Help learn quality management"))
