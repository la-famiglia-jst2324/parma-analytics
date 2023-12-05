"""Defines convencience wrapper to document storage."""

from typing import Any

from parma_analytics.db.mining.engine import get_engine
from parma_analytics.db.mining.internal.models import DocTemplateInstance
from parma_analytics.db.mining.internal.storage import save_document_from_template
from firebase_admin.firestore import firestore as firestore_types


def store_raw_data(
    datasource: str, instance_id: str, *, data: dict[str, Any]
) -> firestore_types.DocumentReference:
    """Store raw data in the database.

    Args:
        datasource: The datasource name.
        instance_id: The instance id.
        data: The raw data.
    """
    engine = get_engine()
    instance = DocTemplateInstance(
        name=instance_id,
        values={
            "mining_trigger": "111222333",
            "status": "pending",
            "data": data,
        },
    )
    return save_document_from_template(
        engine, f"parma/mining/datasource/{datasource}/raw_data/{instance_id}", instance
    )


store_raw_data("reddit", "instancename", data={"test": "test"})
