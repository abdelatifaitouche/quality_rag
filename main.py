from fastapi import FastAPI
from src.api.router import api_router

app = FastAPI(version="v1", title="Quality Assistant")


app.include_router(api_router)


@app.get("")
def routes():
    return "Routes"
