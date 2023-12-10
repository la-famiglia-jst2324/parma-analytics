"""UUID utility functions."""

import datetime
import secrets
import uuid


def generate_uuid() -> str:
    """Generate a uuid."""
    r = str(datetime.datetime.now()) + secrets.token_hex(32)
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, r))
