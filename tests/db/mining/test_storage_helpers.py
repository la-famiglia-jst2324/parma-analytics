from collections.abc import Iterator
from typing import Any, cast
from unittest.mock import patch

import pytest
from firebase_admin.firestore import firestore as firestore_types
from pytest import fixture

from parma_analytics.db.mining.engine import get_engine
from parma_analytics.db.mining.internal.models import (
    DocField,
    DocTemplate,
    DocTemplateInstance,
)
from parma_analytics.db.mining.internal.storage import (
    filter_documents_from_path,
    read_document,
    read_document_from_path,
    resolve_collection_from_path,
    resolve_document_from_path,
    resolve_document_template_from_path,
    save_document_from_template,
    save_validated_document,
)


@fixture(scope="module")
def engine() -> firestore_types.Client:
    yield get_engine()


@fixture(scope="module")
def dummy_collection(
    engine: firestore_types.Client,
) -> Iterator[firestore_types.CollectionReference]:
    coll = engine.collection("test_collection")
    yield coll


@fixture(scope="module")
def dummy_document(
    dummy_collection: firestore_types.CollectionReference,
) -> firestore_types.DocumentReference:
    doc = dummy_collection.document("test_document")
    doc.set({"test_key": "test_value"})
    yield doc
    doc.delete()


@fixture(scope="module")
def dummy_document_template() -> DocTemplate:
    return DocTemplate(
        fields={
            "f1": DocField(name="f1", type="reference"),
            "f2": DocField(name="f2", type="string"),
            "f3": DocField(name="f3", type="string"),
            "f4": DocField(name="f4", type="map"),
        }
    )


@fixture(scope="module")
def dummy_document_payload() -> dict[str, Any]:
    return {
        "f1": "test_value",
        "f2": "test_value",
        "f3": "test_value",
        "f4": {"test_key": "test_value"},
    }


def test_resolve_collection_from_path(
    engine: firestore_types.Client,
    dummy_collection: firestore_types.CollectionReference,
):
    collection = resolve_collection_from_path(engine, "test_collection")
    assert collection is not None
    assert collection.id == dummy_collection.id
    assert [
        cast(firestore_types.DocumentReference, doc).get()
        for doc in collection.list_documents()
    ] == [
        cast(firestore_types.DocumentReference, doc).get()
        for doc in dummy_collection.list_documents()
    ]

    with pytest.raises(AssertionError):
        resolve_collection_from_path(engine, "test_collection/test_document")


def test_resolve_document_from_path(
    engine: firestore_types.Client,
    dummy_document: firestore_types.DocumentReference,
):
    document = resolve_document_from_path(engine, "test_collection/test_document")
    assert document is not None
    assert document.id == dummy_document.id
    assert read_document(document).to_dict() == dummy_document.get().to_dict()

    with pytest.raises(AssertionError):
        resolve_document_from_path(engine, "test_collection")


def test_resolve_document_template_from_path():
    document = resolve_document_template_from_path(
        "parma/mining/datasource/test_source/raw_data/3413"
    )
    assert document is not None
    assert document.fields.keys() == {"mining_trigger", "status", "company_id", "data"}


def test_validate_document():
    pass  # Called in save_validated_document test


def test_save_document():
    pass  # Called in save_validated_document test


def test_save_validated_document(
    dummy_document: firestore_types.DocumentReference,
    dummy_document_template: DocTemplate,
    dummy_document_payload: dict[str, Any],
):
    doc_ref = save_validated_document(
        dummy_document, dummy_document_template.fields, dummy_document_payload
    )
    assert doc_ref is not None
    assert doc_ref.get().to_dict() == dummy_document.get().to_dict()


def test_save_document_from_template(
    engine: firestore_types.Client,
    dummy_document: firestore_types.DocumentReference,
    dummy_document_template: DocTemplate,
    dummy_document_payload: dict[str, Any],
):
    with patch(
        "parma_analytics.db.mining.internal.storage.resolve_document_template_from_path",
        return_value=dummy_document_template,
    ):
        with patch(
            "parma_analytics.db.mining.internal.storage.resolve_document_from_path",
            return_value=dummy_document,
        ):
            doc = save_document_from_template(
                engine,
                "test_collection/test_document",
                DocTemplateInstance(
                    name="test_document", values=dummy_document_payload
                ),
            )
            assert doc is not None


def test_read_document_from_path(
    engine: firestore_types.Client, dummy_document: firestore_types.DocumentReference
):
    with patch(
        "parma_analytics.db.mining.internal.storage.resolve_document_from_path",
        return_value=dummy_document,
    ):
        doc: firestore_types.DocumentSnapshot = read_document_from_path(
            engine, "test_collection/test_document"
        )
        assert doc is not None
        assert doc.exists


def test_filter_documents_from_path(engine: firestore_types.Client):
    res = filter_documents_from_path(
        engine,
        path="parma/mining/datasource/test_source/raw_data",
        filter_name="non_existent_name",
        value="test",
    )
    assert res is not None
    assert len(res) == 0
