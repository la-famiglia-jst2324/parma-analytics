"""Module for JWT (JSON Web Token) handling with specialized focus on analytics.

This module contains the JWTHandler class which is designed to create and verify JWTs.
The creation process is specifically tailored for sourcing/analytics purposes, involving
a two-step JWT creation method using different secret keys. The verification process
supports both shared and analytics secret keys, utilizing an Enum for type safety and
clarity.
"""
import logging
import os
from datetime import datetime, timedelta
from enum import Enum
from typing import Any

from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError

logger = logging.getLogger(__name__)


class KeyType(Enum):
    """Enumeration for JWT key types."""

    SHARED = "shared"
    ANALYTICS = "analytics"


class JWTHandler:
    """A handler for creating and verifying JWTs."""

    SHARED_SECRET_KEY: str = str(os.getenv("ANALYTICS_BASE_URL") or "SHARED_SECRET_KEY")
    ANALYTICS_SECRET_KEY: str = str(
        os.getenv("ANALYTICS_SECRET_KEY") or "ANALYTICS_SECRET_KEY"
    )
    ALGORITHM: str = "HS256"

    @staticmethod
    def create_jwt(sourcing_id: int) -> str:
        """Create a JWT specifically for Sourcing Modules.

        It creates a JWT with 'sourcing_id'.
        Then creates another JWT using this as a payload.
        This enables Authentication/Authorization.

        Args:
            sourcing_id (int): The payload data for the JWT.
                                It is the id of the data sourcing module.

        Returns:
            str: The generated JWT token.
        """
        # First JWT with 'sourcing_id'
        expire = datetime.utcnow() + timedelta(minutes=30)
        analytics_payload = {"sourcing_id": sourcing_id, "exp": expire}
        authorization_jwt = jwt.encode(
            analytics_payload,
            JWTHandler.ANALYTICS_SECRET_KEY,
            algorithm=JWTHandler.ALGORITHM,
        )

        # Second JWT with the first JWT as 'sourcing_id' payload
        shared_payload = {"sourcing_id": authorization_jwt, "exp": expire}
        token = jwt.encode(
            shared_payload, JWTHandler.SHARED_SECRET_KEY, algorithm=JWTHandler.ALGORITHM
        )
        return token

    @staticmethod
    def verify_jwt(token: str, key_type: KeyType) -> dict[str, Any] | None:
        """Verify a JWT using either the shared secret key or the analytics secret key.

        Args:
            token (str): The JWT token to verify.
            key_type (KeyType): The type of key used for verification
                                    (shared or analytics).

        Returns:
            dict[str, Any] | None: The decoded JWT payload
                                            if the verification is successful,
                                            None otherwise.
        """
        secret_key = (
            JWTHandler.ANALYTICS_SECRET_KEY
            if key_type == KeyType.ANALYTICS
            else JWTHandler.SHARED_SECRET_KEY
        )
        try:
            return jwt.decode(token, secret_key, algorithms=[JWTHandler.ALGORITHM])
        except ExpiredSignatureError:
            logging.error("JWT has expired.")
            return None
        except JWTError:
            return None
