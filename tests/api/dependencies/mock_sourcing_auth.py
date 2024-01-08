"""Mock implementations of auth functions for testing.

This module provides mock versions of authentication and authorization functions. These
mock functions are designed for use in test environments where actual authentication and
authorization processes are not required.
"""

from random import randint

from fastapi import Depends, Header

from parma_analytics.api.dependencies.sourcing_auth import authenticate_sourcing_request

mock_authorization_header = {"Authorization": "Bearer dummytoken"}


def mock_authorize_sourcing_request(
    payload: dict[str, str] = Depends(authenticate_sourcing_request)
) -> int:
    """Mock function to simulate authorization in a test environment.

    Args:
        payload: The mock payload for the sourcing authorization request

    Returns:
        A random integer representing a mock source_id for testing purposes.
    """
    return randint(1, 1000)


def mock_authenticate_sourcing_request(
    authorization: str = Header(None),
) -> dict[str, str]:
    """Mock function to simulate authentication in a test environment.

    Args:
        authorization: A mock authorization header.

    Returns:
        A mock JWT payload containing a 'sourcing_id'.
    """
    return {"sourcing_id": "dummytoken"}
