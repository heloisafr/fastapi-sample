from fastapi import APIRouter

router = APIRouter()

items_db = [{"item_name": "One"}, {"item_name": "Two"}, {"item_name": "Tree"}, {"item_name": "Four"}]


@router.get("/items/")
def read_item(skip: int = 0, limit: int = 10):
    """
    Query parameter sample with default value
    """
    return items_db[skip: skip + limit]


@router.get("/things/{item_id}")
def read_things(item_id: int, q: str | None = None):
    """
    Query parameter sample with optional parameter (q)
    q: Union[str, None], quer dizer que "q" pode ser uma string ou None
    Se retirar o "= None" do "q" quebra documentação
    """
    return {"item_id": item_id, "q": q}


@router.get("/artifacts/{item_id}")
def read_things(item_id: int, short_description: bool = False):
    """
    Query parameter sample with default boolean parameter
    """
    item = {"item_id": item_id, "description": "This is a long description"}
    if short_description:
        item.update({"description": "This is a short description"})
    return item


@router.get("/devices/{item_id}")
def read_devices(item_id: int, model: str):
    """
    Query parameter sample with required parameter
    """
    return {"item_id": item_id, "model": model}

