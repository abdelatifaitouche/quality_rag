from fastapi import FastAPI
from src.endpoints.chatbot_endpoint import *


app = FastAPI(version="v1")


@app.get("")
def routes():
    return "Routes"
