"""Defines convencience wrapper to document storage."""

from typing import Any

from firebase_admin.firestore import firestore as firestore_types

from parma_analytics.db.mining.engine import get_engine
from parma_analytics.db.mining.internal.models import DocTemplateInstance
from parma_analytics.db.mining.internal.storage import (
    filter_documents_from_path,
    read_document_from_path,
    save_document_from_template,
)
from parma_analytics.db.mining.models import RawData, RawDataIn
from parma_analytics.utils.uuid import generate_uuid


def store_raw_data(
    datasource: str, *, raw_data: RawDataIn
) -> firestore_types.DocumentReference:
    """Store raw data in the database.

    Args:
        datasource: The datasource name.
        raw_data: The raw data.
    """
    engine = get_engine()
    instance_id = generate_uuid()
    instance = DocTemplateInstance(
        name=instance_id,
        values=dict(raw_data),
    )
    return save_document_from_template(
        engine, f"parma/mining/datasource/{datasource}/raw_data/{instance_id}", instance
    )


def read_raw_data_by_id(datasource: str, instance_id: str) -> dict[str, Any]:
    """Read raw data from the database.

    Args:
        datasource: The datasource name.
        instance_id: The instance id.

    Returns:
        The raw data.
    """
    snapshot = read_document_from_path(
        get_engine(), f"parma/mining/datasource/{datasource}/raw_data/{instance_id}"
    )
    return RawData(
        id=snapshot.id,
        create_time=snapshot.create_time,
        update_time=snapshot.update_time,
        read_time=snapshot.read_time,
        mining_trigger=snapshot.get("mining_trigger"),
        status=snapshot.get("status"),
        company_id=snapshot.get("company_id"),
        data=snapshot.to_dict()["data"],
    )


def read_raw_data_by_company(datasource: str, company_id: str) -> list[dict[str, Any]]:
    """Read all raw data for a company from the database.

    Args:
        datasource: The datasource name.
        company_id: The company id.

    Returns:
        List of raw data.
    """
    filtered_documents = filter_documents_from_path(
        get_engine(),
        f"parma/mining/datasource/{datasource}/raw_data",
        "company_id",
        company_id,
    )

    response = []
    for filtered_document in filtered_documents:
        response.append(read_raw_data_by_id(datasource, filtered_document.id))

    return response
