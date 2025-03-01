from enum import Enum
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class CNNName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/items/book")
def read_item_book():
    """
    Path parameter sample
    The order matter!
        Path operations are evaluated in order,
        you need to make sure that the path for /items/book is declared before the one for /items/{item_id}.
        Otherwise, the path for /items/{item_id} would match also for /items/book,
        "thinking" that it's receiving a parameter item_id with a value of "book"
    """
    return {"item_id": "book"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    """
    Path parameter sample
    Não há necessidade de validação (tipagem ou obrigatoria) das entradas,
    o framework faz isso para você
    """
    return {"item_id": item_id}


@app.get("/models/{model_name}")
def get_model(model_name: CNNName):
    """
    Path parameter sample using Enum as input
    """
    if model_name.value == "alexnet":
        message = "AlextNet is the first best CNN"
    elif model_name is CNNName.lenet:
        message = "Lenet is first CNN"
    else:
        message = "Residual CNN"

    # You can return enum members from your path operation,
    # they will be converted to their corresponding values before returning them to the client
    return  {"model_name": model_name, "message": message}


@app.get("/files/{file_path:path}")
def get_file(file_path: str):
    """
    Path parameter containing a path
    """
    return {"file_path": file_path}


"""
q: Union[str, None], quer dizer que "q" pode ser uma string ou None
Se retirar o "= None" do q dá pau na documentação"""
# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None
# is_offer: Union[bool, None], que dizer que is_offer pode ser um boll ou None

# Não precisa validação (tipo e obrigatoria) das entradas, o framework faz isso para vc
# pode-se usar um tipo complexo (json) como entrada, por ex: Item
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_price": item.price, "item_id": item_id}

