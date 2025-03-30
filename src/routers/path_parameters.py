from enum import Enum
from fastapi import APIRouter, Path
from typing import Annotated


router = APIRouter()


class CNNName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@router.get("/items/book")
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


@router.get("/items/{item_id}")
def read_item(item_id: int):
    """
    Path parameter sample
    Não há necessidade de validação (tipagem ou obrigatoria) das entradas,
    o framework faz isso para você
    """
    return {"item_id": item_id}


@router.get("/devices/{device_id}")
def read_devices(device_id: Annotated[int, Path(ge=1, lt=1000)]):
    """
    Path parameter sample with "greater than or equal" and "less than" validation
    The same applies for gt "greater than" and le "less than or equal"
    """
    return {"device_id": device_id}


@router.get("/models/{model_name}")
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


@router.get("/files/{file_path:path}")
def get_file(file_path: str):
    """
    Path parameter containing a path
    """
    return {"file_path": file_path}
