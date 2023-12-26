from collections.abc import Iterator

import pytest
from google.cloud import secretmanager

from parma_analytics.utils.uuid import generate_uuid
from parma_analytics.vendor.gcp import PROJECT_ID
from parma_analytics.vendor.secret_manager import (
    get_client,
    retrieve_secret,
    store_secret,
)


@pytest.fixture(scope="module")
def secret_client() -> Iterator[secretmanager.SecretManagerServiceClient]:
    yield get_client()


@pytest.fixture
def entropy_token() -> Iterator[str]:
    yield generate_uuid()


def test_encrypt_decrypt(
    secret_client: secretmanager.SecretManagerServiceClient, entropy_token: str
):
    secret_id = f"parma-analytics-ci-test-{entropy_token}"
    secret_value = "test_value"
    store_secret(secret_client, secret_id=secret_id, secret_value=secret_value)

    read_secret = retrieve_secret(secret_client, secret_id=secret_id)
    assert read_secret == secret_value

    # new value
    new_secret_value = "test_value2"
    store_secret(secret_client, secret_id=secret_id, secret_value=new_secret_value)

    read_secret = retrieve_secret(secret_client, secret_id=secret_id)
    assert read_secret == new_secret_value

    # cleanup
    secret_client.delete_secret(
        request={"name": secret_client.secret_path(PROJECT_ID, secret_id)}
    )
