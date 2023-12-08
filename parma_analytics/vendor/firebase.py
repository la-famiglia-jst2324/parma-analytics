"""Firebase module to handle firebase app creation."""

import json
import os
from pathlib import Path

import firebase_admin
from firebase_admin import credentials

MODULE_DIR = Path(__file__).parent
PROJECT_ROOT = MODULE_DIR.parents[1]
CREDENTIALS_PATH = (
    PROJECT_ROOT / ".secrets" / "la-famiglia-parma-ai-firebase-adminsdk.json"
)


def get_app() -> firebase_admin.App:
    """Retrieves the firebase app.

    Creates a new app if one does not exist.

    Returns:
        firebase_admin.App: The firebase app.
    """
    app = _try_get_app()
    if not app:
        return _init_firebase()
    return app


# ------------------------------------- Internal ------------------------------------- #


def _init_firebase() -> firebase_admin.App:
    env_var = os.environ.get("FIREBASE_ADMINSDK_CERTIFICATE")
    fb_certificate = credentials.Certificate(
        json.loads(env_var) if env_var else CREDENTIALS_PATH
    )
    return firebase_admin.initialize_app(fb_certificate)


def _try_get_app() -> firebase_admin.App:
    try:
        return firebase_admin.get_app()

    except ValueError as e:
        if "The default Firebase app does not exist" in str(e):
            return None
        raise e
