"""Storage helpers."""

from datetime import datetime
from typing import Any, Literal, overload

from firebase_admin.firestore import firestore as firestore_types

from parma_analytics.db.mining.internal.models import (
    Collection,
    Doc,
    DocField,
    DocTemplate,
    DocTemplateInstance,
)

from .definitions import parma_collection


def resolve_collection_from_path(
    engine: firestore_types.Client, path: str
) -> firestore_types.CollectionReference:
    """Resolve a collection from a path.

    Args:
        engine: The database engine.
        path: The path to resolve. (e.g. "parma/mining/datasource")
    """
    return _resolve_from_path(engine, path, document=False)


def resolve_document_from_path(
    engine: firestore_types.Client, path: str
) -> firestore_types.DocumentReference:
    """Resolve a document from a path.

    Args:
        engine: The database engine.
        path: The path to resolve. (e.g. "mining/mining")
    """
    return _resolve_from_path(engine, path, document=True)


def resolve_document_template_from_path(
    engine: firestore_types.Client, path: str
) -> DocTemplate:
    """Resolve a document template from a path.

    Args:
        engine: The database engine.
        path: The path to resolve. (e.g. "mining/mining")
    """
    path_parts = _split_path(path)
    assert len(path_parts) % 2 == 0, "Path must be odd length to lead to a collection"
    assert path_parts[0] == "parma", "Path must start with 'parma'"
    path_parts = path_parts[1:]

    # traversing parma_collection
    cur_item: Doc | DocTemplate | Collection = parma_collection
    for part in path_parts:
        if isinstance(cur_item, Collection):
            if isinstance(cur_item.docs, DocTemplate):
                cur_item = cur_item.docs  # name does not matter
            else:
                cur_item = cur_item.docs[part]
        elif isinstance(cur_item, DocTemplate):
            cur_item = cur_item.collections[part]
        elif isinstance(cur_item, Doc):
            cur_item = cur_item.collections[part]
        else:
            raise ValueError(f"Unknown type: {type(cur_item)}")

    assert isinstance(cur_item, DocTemplate)
    return cur_item


def validate_document(
    engine: firestore_types.Client, fields: dict[str, DocField], values: dict[str, Any]
) -> dict[str, Any]:
    """Validates a document for firestore and raises ValueError if invalid.

    Returns:
        Dictionary payload on success.
    """
    payload: dict[str, Any] = {}
    for field_name, field in fields.items():
        assert field_name == field.name
        # validation
        val: Any = values.get(field.name)

        # validate types
        if field.type == "string":
            if not isinstance(val, str):
                raise ValueError(f"Expected type {field.type} but got {type(val)}")
        elif field.type == "number":
            if not isinstance(val, int) or not isinstance(val, float):
                raise ValueError(f"Expected type {field.type} but got {type(val)}")
        elif field.type == "boolean":
            if not isinstance(val, bool):
                raise ValueError(f"Expected type {field.type} but got {type(val)}")
        elif field.type == "timestamp":
            if not isinstance(val, datetime):
                raise ValueError(f"Expected type {field.type} but got {type(val)}")
        elif field.type == "array":
            if not isinstance(val, list):
                raise ValueError(f"Expected type {field.type} but got {type(val)}")
        elif field.type == "map":
            if not isinstance(val, dict):
                raise ValueError(f"Expected type {field.type} but got {type(val)}")
        elif field.type == "null":
            if val is not None:
                raise ValueError(f"Expected type {field.type} but got {type(val)}")
        elif field.type == "geopoint":
            raise NotImplementedError("Not implemented")
        elif field.type == "reference":
            if not isinstance(val, str):
                raise ValueError(f"Expected type {field.type} but got {type(val)}")
        else:
            raise ValueError(f"Unknown type: {field.type}")

        payload[field.name] = val

    return payload


def save_document(
    fs_doc: firestore_types.DocumentReference, payload: dict[str, Any]
) -> firestore_types.DocumentReference:
    """Save a document to firestore.

    Args:
        fs_doc: The firestore document.
        payload: The document payload.
    """
    fs_doc.set(payload)
    return fs_doc


def save_document_from_template(
    engine: firestore_types.Client,
    path: str,
    instance: DocTemplateInstance,
) -> firestore_types.DocumentReference:
    """Save a document to firestore.

    Args:
        engine: The database engine.
        path: The document path. (e.g. "mining/datasource/raw_data/2340923741209")
        payload: The document payload.
    """
    doc_template = resolve_document_template_from_path(engine, path)
    fs_doc: firestore_types.DocumentReference = resolve_document_from_path(engine, path)
    payload = validate_document(engine, doc_template.fields, instance.values)
    return save_document(fs_doc, payload)


# ------------------------------------------------------------------------------------ #
#                                       Internal                                       #
# ------------------------------------------------------------------------------------ #


def _split_path(path: str) -> list[str]:
    """Split a path into parts.

    Args:
        path: The path to split. (e.g. "parma/mining/datasource")

    Returns:
        The path parts.
    """
    return path.removeprefix("/").removesuffix("/").split("/")


@overload
def _resolve_from_path(
    engine: firestore_types.Client,
    path: str,
    document: Literal[False],
) -> firestore_types.CollectionReference:
    ...


@overload
def _resolve_from_path(
    engine: firestore_types.Client, path: str, document: Literal[True]
) -> firestore_types.DocumentReference:
    ...


def _resolve_from_path(
    engine: firestore_types.Client, path: str, document: bool
) -> firestore_types.CollectionReference | firestore_types.DocumentReference:
    path_parts = _split_path(path)
    assert len(path_parts) % 2 == (
        0 if document else 1
    ), "Path must be odd length to lead to a collection"

    current_ref = engine

    # as we alternate between collections and documents, we need to store the state
    at_collection = True

    for part in path_parts:
        if at_collection:
            current_ref = current_ref.collection(part)
        else:
            current_ref = current_ref.document(part)
        at_collection = not at_collection
    return current_ref
