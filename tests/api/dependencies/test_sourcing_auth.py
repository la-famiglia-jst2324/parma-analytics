from unittest.mock import patch

import pytest
from fastapi import HTTPException, status

from parma_analytics.api.dependencies.sourcing_auth import (
    authenticate_sourcing_request,
    authorize_sourcing_request,
)


def test_authenticate_sourcing_request_invalid_token():
    with patch(
        "parma_analytics.api.dependencies.sourcing_auth.JWTHandler.verify_jwt",
        return_value=None,
    ):
        with pytest.raises(HTTPException) as exc:
            authenticate_sourcing_request("Bearer invalid_token")
    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Invalid shared token or expired token" in str(exc.value.detail)


@pytest.mark.parametrize(
    "token, expected_return",
    [
        ("Bearer valid_token", "valid_token"),
        ("valid_token", "valid_token"),
        ("Bearer xya", "xya"),
        ("xya", "xya"),
    ],
)
def test_authenticate_valid_token(token, expected_return):
    with patch(
        "parma_analytics.api.dependencies.sourcing_auth.JWTHandler.verify_jwt",
        return_value=expected_return,
    ):
        assert authenticate_sourcing_request(token) == expected_return


@pytest.mark.parametrize(
    "authorization, payload",
    [
        (
            "Bearer valid_token",
            {
                "sourcing_id": {
                    "sourcing_id": "1",
                },
            },
        ),
    ],
)
def test_authenticate_sourcing_request_valid_token(authorization, payload):
    with patch(
        "parma_analytics.api.dependencies.sourcing_auth.authenticate_sourcing_request",
        return_value=payload,
    ):
        with patch(
            "parma_analytics.api.dependencies.sourcing_auth.JWTHandler.verify_jwt",
            return_value=payload.get("sourcing_id"),
        ):
            assert authenticate_sourcing_request(authorization) == payload.get(
                "sourcing_id"
            )


@pytest.mark.parametrize(
    "authorization, payload",
    [
        (
            "Bearer valid_token",
            {
                "x": "y",
            },
        ),
    ],
)
def test_authenticate_sourcing_request_invalid_token_first(authorization, payload):
    with patch(
        "parma_analytics.api.dependencies.sourcing_auth.JWTHandler.verify_jwt",
        return_value=payload.get("sourcing_id"),
    ):
        with pytest.raises(HTTPException) as exc:
            authenticate_sourcing_request(authorization)
        assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid shared token or expired token" in str(exc.value.detail)


@pytest.mark.parametrize(
    "authorization, payload",
    [
        (
            "Bearer valid_token",
            {
                "x": "y",
            },
        ),
    ],
)
def test_authorize_sourcing_request_bad_request(authorization, payload):
    with patch(
        "parma_analytics.api.dependencies.sourcing_auth.JWTHandler.verify_jwt",
        return_value=payload.get("sourcing_id"),
    ):
        with pytest.raises(HTTPException) as exc:
            authorize_sourcing_request(payload)
        assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "Authorization token not found in shared token" in str(exc.value.detail)


@pytest.mark.parametrize(
    "authorization, payload",
    [
        (
            "Bearer valid_token",
            {
                "sourcing_id": {
                    "x": "y",
                },
            },
        ),
    ],
)
def test_authorize_sourcing_request_invalid_token_second(authorization, payload):
    with patch(
        "parma_analytics.api.dependencies.sourcing_auth.JWTHandler.verify_jwt",
        return_value=payload.get("sourcing_id"),
    ):
        with pytest.raises(HTTPException) as exc:
            authorize_sourcing_request(payload)
        assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "source_id not found in authorization token" in str(exc.value.detail)


@pytest.mark.parametrize(
    "authorization, payload",
    [
        (
            "Bearer valid_token",
            {
                "sourcing_id": {
                    "sourcing_id": "abc",
                },
            },
        ),
    ],
)
def test_authorize_sourcing_request_invalid_token_third(authorization, payload):
    with patch(
        "parma_analytics.api.dependencies.sourcing_auth.JWTHandler.verify_jwt",
        return_value=payload.get("sourcing_id"),
    ):
        with pytest.raises(HTTPException) as exc:
            authorize_sourcing_request(payload)
        assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "source_id in authorization token is not a valid integer" in str(
            exc.value.detail
        )


@pytest.mark.parametrize(
    "authorization, payload",
    [
        (
            "Bearer valid_token",
            {
                "sourcing_id": {
                    "sourcing_id": "abc",
                },
            },
        ),
    ],
)
def test_authorize_sourcing_request_invalid_token_forth(authorization, payload):
    with patch(
        "parma_analytics.api.dependencies.sourcing_auth.JWTHandler.verify_jwt",
        return_value=None,
    ):
        with pytest.raises(HTTPException) as exc:
            authorize_sourcing_request(payload)
        assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid authorization token or expired token" in str(exc.value.detail)


@pytest.mark.parametrize(
    "authorization, payload",
    [
        (
            "Bearer valid_token",
            {
                "sourcing_id": {
                    "sourcing_id": "123",
                },
            },
        ),
    ],
)
def test_authorize_sourcing_request_valid_token(authorization, payload):
    with patch(
        "parma_analytics.api.dependencies.sourcing_auth.JWTHandler.verify_jwt",
        return_value=payload.get("sourcing_id"),
    ):
        response = authorize_sourcing_request(payload)
        assert str(response) == payload.get("sourcing_id").get("sourcing_id")
