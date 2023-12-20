"""This module contains authentication and authorization dependencies.

Specifically designed for sourcing modules in the FastAPI application, it includes
functions to authenticate requests using JWTs and to authorize these requests by
validating the JWTs against defined secret keys. The module ensures that only valid and
authorized sourcing modules can access certain endpoints.
"""

from fastapi import Depends, HTTPException, Header, status

from parma_analytics.utils.jwt_handler import JWTHandler, KeyType


async def authenticate_sourcing_request(
    authorization: str = Header(...),
) -> dict[str, str]:
    """Authenticate the incoming request using the JWT in the Authorization header.

    Args:
        authorization (str): The Authorization header containing the JWT.

    Returns:
        Dict[str, str | int]: The payload of the authenticated JWT.

    Raises:
        HTTPException: If the JWT is invalid or expired.
    """
    token = (
        authorization.split(" ")[1]
        if authorization.startswith("Bearer ")
        else authorization
    )
    payload = JWTHandler.verify_jwt(token, key_type=KeyType.SHARED)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid shared token or expired token",
        )
    return payload


async def authorize_sourcing_request(
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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authorization token not found in shared token",
        )

    auth_payload = JWTHandler.verify_jwt(auth_token, key_type=KeyType.ANALYTICS)
    if auth_payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization token or expired token",
        )

    source_id = auth_payload.get("sourcing_id")
    if not source_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="source_id not found in authorization token",
        )

    # Ensure source_id is an integer
    if isinstance(source_id, str):
        try:
            source_id = int(source_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="source_id in authorization token is not a valid integer",
            )

    return source_id
