import logging
from typing import Literal

import pytest
from fastapi.testclient import TestClient
from starlette import status

logger = logging.getLogger(__name__)


@pytest.mark.parametrize("name", ["", "foo", "bar"])
@pytest.mark.parametrize("price", [-1, 0, 3.0, 100.4])
@pytest.mark.parametrize("is_offer", [True, False])
@pytest.mark.parametrize("endpoint", ["create", "update"])
def test_create_update_dummy(
    client: TestClient,
    endpoint: Literal["create", "update"],
    name: str,
    price: float,
    is_offer: bool,
):
    if endpoint == "create":
        response = client.post(
            "/dummy",
            json={"name": name, "price": price, "is_offer": is_offer},
        )
    else:
        response = client.put(
            "/dummy/1",
            json={"name": name, "price": price, "is_offer": is_offer},
        )

    if not name:
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "String should have at least 1 character" in str(response.json())
        return

    if price < 0:
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "Input should be greater than or equal to 0" in str(response.json())
        return

    assert (
        response.status_code == status.HTTP_201_CREATED
        if endpoint == "create"
        else status.HTTP_202_ACCEPTED
    )
    assert response.json() == {
        "id": 1,
        "name": name,
        "price": price,
        "is_offer": is_offer,
    }


def test_read_dummy(client: TestClient):
    response = client.get("/dummy/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 1,
        "name": "foo",
        "price": 42,
        "is_offer": True,
    }


def test_delete_dummy(client: TestClient):
    response = client.delete("/dummy/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
