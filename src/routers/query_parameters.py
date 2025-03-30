from fastapi import APIRouter, Query
from pydantic import BaseModel, Field
from typing import Annotated, Literal

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


@router.get("/things/")
def read_things(skip: int = 0, limit: int = 10):
    """
    Optional query parameter (skip and limit) with default value
    """
    return items_db[skip: skip + limit]


@router.get("/things/{item_id}/{serial}/{type}")
def read_things(item_id: int, serial: int, type: str, short_description: bool = False):
    """
    Optional query parameter (short_description) with default boolean parameter
    """
    item = {"item_id": item_id, "serial": serial, "type": type, "description": "This is a long description"}
    if short_description:
        item.update({"description": "This is a short description"})
    return item


@router.get("/things/{item_id}/{serial}")
def read_things(item_id: int, serial: int, q: Annotated[ str | None, Query(min_length=4, max_length=9, pattern="something")] = None):
    """
    Optional query parameter (q) with min_length, max_length and pattern validation
    Whenever "q" is provided its length cannot exceed 10 and must have at least 4 characters
    q: str | None means that "q" can be a string or None
    """
    return {"item_id": item_id, "serial": serial, "q": q}


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


@router.get("/artifacts")
def read_artifacts(model: Annotated[list[str] | None, Query()] = None):
    """
    Query parameter (model) that receive a list of values
    """
    return {"model": model}


@router.get("/artifacts/{item_id}")
def read_artifacts(
        item_id: int,
        model: Annotated[list[str] | None,
            Query(
                title="Models",
                description="A model list",
                alias="models-list",
                deprecated=True,
                include_in_schema=True
            )] = None):
    """
    Query parameter (model) that receive a list of values
    This sample include metadata: title, description, deprecated and alias.
    They are optional and used by documentation user interfaces
    The "alias" models-list must be used in the requisition instead model
        like this: http://127.0.0.1:8000/artifacts/1/?models-list=foo
    The "include_in_schema" if setup to False will hide the model param from documentation user interfaces
    """
    return {"item_id": item_id, "model": model}


class FilterParams(BaseModel):

    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []

    # it is optional
    # means that any extra parameter wont be acceptable and an error will be fire
    model_config = {"extra": "forbid"}


@router.get("/items")
def read_items(filter_query: Annotated[FilterParams, Query()]):
    """
    Sample using a pydantic model
    The advantage is that models are reusable
    """
    return filter_query