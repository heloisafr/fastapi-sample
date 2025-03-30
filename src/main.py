from fastapi import FastAPI
from src.routers import (request_body,
                         path_parameters,
                         query_parameters,
                         custom_validation)

app = FastAPI()
app.include_router(request_body.router)
app.include_router(path_parameters.router, prefix='/path')
app.include_router(query_parameters.router, prefix='/query')
app.include_router(custom_validation.router, prefix='/custom-validation')


@app.get("/")
def home():
    return {"msg": "The API is up!"}
