from enum import Enum
from fastapi import APIRouter

router = APIRouter()


class CNNName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@router.get("/items/book")
def read_item_book() -> None:
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
def read_item(item_id: int) -> None:
    """
    Path parameter sample
    Não há necessidade de validação (tipagem ou obrigatoria) das entradas,
    o framework faz isso para você
    """
    return {"item_id": item_id}


@router.get("/models/{model_name}")
def get_model(model_name: CNNName) -> None:
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
def get_file(file_path: str) -> None:
    """
    Path parameter containing a path
    """
    return {"file_path": file_path}
