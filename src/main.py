from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def home():
    return {"msg": "The API is up!"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    """
    Não há necessidade de validação (tipagem ou obrigatoria) das entradas,
    o framework faz isso para você
    """
    return {"item_id": item_id}


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

