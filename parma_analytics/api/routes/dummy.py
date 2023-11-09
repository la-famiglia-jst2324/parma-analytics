"""Main entrypoint for the API routes in of parma-analytics."""

from fastapi import APIRouter

from parma_analytics.api.models.dummy import (
    ApiDummyCreateIn,
    ApiDummyCreateOut,
    ApiDummyOut,
    ApiDummyUpdateIn,
    ApiDummyUpdateOut,
)

router = APIRouter()


@router.post("/dummy", status_code=201)
def create_dummy(dummy: ApiDummyCreateIn) -> ApiDummyCreateOut:
    """Dummy POST entrpoint for the API.

    Args:
        dummy: The dummy object to create.
    """
    # hand over to business logic layer and transform the result to the API model again
    return ApiDummyCreateOut(
        id=1,  # given by database layer through business logic layer
        name=dummy.name,
        price=dummy.price,
        is_offer=dummy.is_offer,
    )


@router.get("/dummy/{dummy_id}", status_code=200)
def read_dummy(dummy_id: int) -> ApiDummyOut:
    """Dummy GET entrpoint for the API.

    Args:
        dummy_id: The ID of the dummy.
    """
    # fetch from the database layer through the business logic layer
    return ApiDummyOut(id=dummy_id, name="Foo", price=42, is_offer=True)


@router.put("/dummy/{dummy_id}", status_code=202)
def update_dummy(dummy_id: int, dummy: ApiDummyUpdateIn) -> ApiDummyUpdateOut:
    """Dummy PUT entrpoint for the API.

    Args:
        dummy_id: The ID of the dummy.
        dummy: The dummy object to update.
    """
    # hand over to business logic layer and transform the result to the API model again
    return ApiDummyUpdateOut(
        id=dummy_id, name=dummy.name, price=dummy.price, is_offer=dummy.is_offer
    )


@router.delete("/dummy/{dummy_id}", status_code=204)
def delete_dummy(dummy_id: int) -> None:
    """Dummy DELETE entrpoint for the API.

    Args:
        dummy_id: The ID of the dummy.
    """
    # hand over to business logic layer
    pass
