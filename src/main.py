from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def home():
    return {"msg": "The API is up!"}


# Não precisa validação (tipo e obrigatoria) das entradas, o framework faz isso para vc
# q: Union[str, None], quer dizer que q pode ser uma string ou None
# Eu consegui dar pau nos docs ao retirar o "= None" do q
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

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

