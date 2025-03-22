from fastapi import APIRouter, Query
from typing import Annotated

router = APIRouter()

items_db = [{"item_name": "One"}, {"item_name": "Two"}, {"item_name": "Tree"}, {"item_name": "Four"}]


@router.get("/things/{item_id}")
def read_things(item_id: int, q: str | None = None):
    """
    Optional query parameter (q)
    q: str | None means that "q" can be a string or None
    Se retirar o "= None" do "q" quebra documentação
    """
    return {"item_id": item_id, "q": q}


@router.get("/items/")
def read_items(skip: int = 0, limit: int = 10):
    """
    Optional query parameter (skip and limit) with default value
    """
    return items_db[skip: skip + limit]


@router.get("/artifacts/{item_id}")
def read_artifacts(item_id: int, short_description: bool = False):
    """
    Optional query parameter (short_description) with default boolean parameter
    """
    item = {"item_id": item_id, "description": "This is a long description"}
    if short_description:
        item.update({"description": "This is a short description"})
    return item


@router.get("/things")
def read_things(q: Annotated[ str | None, Query(min_length=4, max_length=9, pattern="something")] = None):
    """
    Optional query parameter (q) with min_length, max_length and pattern validation
    Whenever "q" is provided its length cannot exceed 10 and must have at least 4 characters
    q: str | None means that "q" can be a string or None
    """
    return {"q": q}


@router.get("/devices/{item_id}")
def read_devices(item_id: int, model: str):
    """
    Query parameter (model) with required parameter
    Even sending model=None it is valid
    """
    return {"item_id": item_id, "model": model}


@router.get("/devices")
def read_devices(model: Annotated[str, Query(min_length=4)]):
    """
    Query parameter (model) with required parameter and min_length validation
    """
    return {"model": model}


@router.get("/devices/{item_id}/{serial}")
def read_devices(item_id: int, serial: int, model: Annotated[str | None, Query(min_length=5)]):
    """
    Query parameter (model) with required parameter and min_length validation
    Even though required can me None
    (There was no different between this and the previous function in test cases)
    """
    return {"item_id": item_id, "serial": serial, "model": model}

