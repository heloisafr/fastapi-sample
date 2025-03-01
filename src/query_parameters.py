from enum import Enum
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

items_db = [{"item_name": "One"}, {"item_name": "Two"}, {"item_name": "Tree"}, {"item_name": "Four"}]


@app.get("/items/")
def read_item(skip: int = 0, limit: int = 10):
    """
    Query parameter sample
    """
    return items_db[skip: skip + limit]
