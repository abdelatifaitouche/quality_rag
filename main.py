from fastapi import FastAPI


app = FastAPI(version="v1")


@app.get("")
def routes():
    return "Routes"
