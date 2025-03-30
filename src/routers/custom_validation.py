from typing import Annotated

from fastapi import APIRouter
from pydantic import AfterValidator

router = APIRouter()

data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}


def check_valid_id(id: str):
    if not id.startswith(("isbn-", "imdb-")):
        raise ValueError('Invalid ID format, it must start with "isbn-" or "imdb-"')
    return id


@router.get("/items/")
def read_items(id: Annotated[str | None, AfterValidator(check_valid_id)]):
    """
    Custom validation
    more about pydantic validators:
        https://docs.pydantic.dev/latest/concepts/validators/#field-validators
    """
    item = data.get(id)
    return {"id": id, "name": item}

