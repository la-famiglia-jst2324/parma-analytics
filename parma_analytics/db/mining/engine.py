"""Module for interacting with firestore engines."""

from firebase_admin import firestore
from firebase_admin.firestore import firestore as firestore_types
from parma_analytics.vendor.firebase import get_app


def get_engine() -> firestore_types.Client:
    """Retrieves the firestore engine from the firebase app.

    Returns:
        The firestore engine.
    """
    app = get_app()
    engine = firestore.client(app)
    return engine
