"""This module contains authentication and authorization dependencies.

Specifically designed for sourcing modules in the FastAPI application, it includes
functions to authenticate requests using JWTs and to authorize these requests by
validating the JWTs against defined secret keys. The module ensures that only valid and
authorized sourcing modules can access certain endpoints.
"""
import logging

from fastapi import Depends, HTTPException, Header, status

from parma_analytics.utils.jwt_handler import JWTHandler, KeyType

logger = logging.getLogger(__name__)


def authenticate_sourcing_request(
    authorization: str = Header(None),
) -> dict[str, str]:
    """Authenticate the incoming request using the JWT in the Authorization header.

    Args:
        authorization (str): The Authorization header containing the JWT.

    Returns:
        Dict[str, str | int]: The payload of the authenticated JWT.

    Raises:
        HTTPException: If the JWT is invalid or expired.
        HTTPException: If the Authorization header is missing.
    """
    if authorization is None:
        logger.error("Authorization header is required!")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is required!",
        )

    token = (
        authorization.split(" ")[1]
        if authorization.startswith("Bearer ")
        else authorization
    )
    payload = JWTHandler.verify_jwt(token, key_type=KeyType.SHARED)
    if payload is None:
        logger.error("Invalid shared token or expired token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid shared token or expired token",
        )
    return payload


def authorize_sourcing_request(
    payload: dict[str, str] = Depends(authenticate_sourcing_request)
) -> int:
    """Authorize the request based on the JWT payload obtained from authentication.

    Args:
        payload (Dict[str, str]): The payload from the authenticated JWT.

    Returns:
        int: The extracted source_id indicating the caller module.

    Raises:
        HTTPException: If the authorization JWT is invalid,
                            expired,
                            or lacks a source_id.
    """
    auth_token = payload.get("sourcing_id")
    if not auth_token:
        logger.error("Authorization token not found in shared token")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authorization token not found in shared token",
        )

    auth_payload = JWTHandler.verify_jwt(auth_token, key_type=KeyType.ANALYTICS)
    if auth_payload is None:
        logger.error("Invalid authorization token or expired token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization token or expired token",
        )

    source_id = auth_payload.get("sourcing_id")
    if not source_id:
        logger.error("source_id not found in authorization token")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="source_id not found in authorization token",
        )

    # Ensure source_id is an integer
    if isinstance(source_id, str):
        try:
            source_id = int(source_id)
        except ValueError:
            logger.error(
                "source_id in authorization token is not a valid integer: %s", source_id
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="source_id in authorization token is not a valid integer",
            )

    return source_id
