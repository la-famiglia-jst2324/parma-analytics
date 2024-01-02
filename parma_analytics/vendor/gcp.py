"""Google Cloud Platform credentials helper.

This module provides a helper function to get credentials for Google Cloud.
"""

import json
import os
from pathlib import Path

from google.oauth2 import service_account

PROJECT_ID = "447443547509"

SECRETS_DIR = Path(__file__).parents[2] / ".secrets"
CREDENTIALS_PATH = SECRETS_DIR / "la-famiglia-parma-ai-secret-manager.json"


def get_credentials() -> service_account.Credentials:
    """Get credentials for Google Cloud Platform."""
    env_var = os.environ.get("GCP_SECRET_MANAGER_CERTIFICATE")
    if env_var:
        credentials = service_account.Credentials.from_service_account_info(
            json.loads(env_var)
        )
    elif CREDENTIALS_PATH.exists():
        credentials = service_account.Credentials.from_service_account_file(
            CREDENTIALS_PATH
        )
    else:
        raise FileNotFoundError(
            f"Credentials file not found at {CREDENTIALS_PATH}. "
            "Please set the environment variable GCP_SECRET_MANAGER_CERTIFICATE "
            "to the JSON string of the credentials."
        )
    return credentials
