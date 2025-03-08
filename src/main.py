from fastapi import FastAPI
from src.routers import request_body, path_parameters, query_parameters

app = FastAPI()
app.include_router((request_body.router))
app.include_router((path_parameters.router))
app.include_router((query_parameters.router))


@app.get("/")
def home():
    return {"msg": "The API is up!"}
