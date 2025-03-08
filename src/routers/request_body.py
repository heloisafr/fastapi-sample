from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float


@router.post("/items/")
def create_item(item: Item):
    """
    Sample of request body
    Usando um tipo complexo (json) como entrada (Item)
    """
    return item


@router.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    """
    Sample of request body + path parameter
    Usando um tipo complexo (json) como entrada (Item)

    Explaining **item.model_dump()
    The item.model_dump() method converts the Pydantic model into a Python dictionary
    The ** operator is used to unpack the key-value pairs from item.model_dump() and merge them into the dictionary
    """
    return {"item_id": item_id, **item.model_dump()}


@router.put("/models/{item_id}")
def update_model(item_id: int, item: Item, q: str):
    """
    Sample of request body + path parameter + query parameter
    Usando um tipo complexo (json) como entrada (Item)
    """
    return {"item_id": item_id, "q": q, **item.model_dump()}

