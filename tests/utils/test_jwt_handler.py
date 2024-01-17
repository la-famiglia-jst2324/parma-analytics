import logging
from unittest.mock import ANY, call, patch

import pytest
from jose.exceptions import ExpiredSignatureError, JWTError

from parma_analytics.utils.jwt_handler import JWTHandler, KeyType


@pytest.fixture
def source_id_int():
    return 123


@pytest.fixture
def mock_jwt():
    return "mock.jwt.token"


@pytest.fixture
def valid_jwt():
    return "valid.jwt.token"


@pytest.fixture
def expired_jwt():
    return "expired.jwt.token"


@pytest.fixture
def invalid_jwt():
    return "invalid.jwt.token"


def test_create_jwt(source_id_int, mock_jwt):
    with patch("jose.jwt.encode", return_value=mock_jwt) as mock_encode:
        jwt = JWTHandler.create_jwt(source_id_int)
        assert jwt == mock_jwt

        first_call = call(
            {"sourcing_id": source_id_int, "exp": ANY},
            JWTHandler.ANALYTICS_SECRET_KEY,
            algorithm=JWTHandler.ALGORITHM,
        )

        second_call = call(
            {"sourcing_id": mock_jwt, "exp": ANY},
            JWTHandler.SHARED_SECRET_KEY,
            algorithm=JWTHandler.ALGORITHM,
        )

        mock_encode.assert_has_calls([first_call, second_call], any_order=False)


def test_verify_jwt_valid(valid_jwt):
    with patch("jose.jwt.decode", return_value=valid_jwt) as mock_decode:
        result = JWTHandler.verify_jwt(valid_jwt, KeyType.SHARED)
        assert result == valid_jwt
        mock_decode.assert_called_once_with(
            valid_jwt, JWTHandler.SHARED_SECRET_KEY, algorithms=[JWTHandler.ALGORITHM]
        )


def test_verify_jwt_expired(expired_jwt, caplog):
    with patch("jose.jwt.decode", side_effect=ExpiredSignatureError) as mock_decode:
        with caplog.at_level(logging.ERROR):
            result = JWTHandler.verify_jwt(expired_jwt, KeyType.SHARED)
            assert result is None
            assert "JWT has expired." in caplog.text
        mock_decode.assert_called_once_with(
            expired_jwt, JWTHandler.SHARED_SECRET_KEY, algorithms=[JWTHandler.ALGORITHM]
        )


def test_verify_jwt_invalid(invalid_jwt):
    with patch("jose.jwt.decode", side_effect=JWTError) as mock_decode:
        result = JWTHandler.verify_jwt(invalid_jwt, KeyType.SHARED)
        assert result is None
        mock_decode.assert_called_once_with(
            invalid_jwt, JWTHandler.SHARED_SECRET_KEY, algorithms=[JWTHandler.ALGORITHM]
        )
