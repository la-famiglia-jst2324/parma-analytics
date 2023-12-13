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
    fields: dict[str, DocField], values: dict[str, Any]
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
        str_types = {
            "string": str,
            "number": int,
            "boolean": bool,
            "timestamp": datetime,
            "array": list,
            "map": dict,
            "null": None,
            "geopoint": None,
            "reference": str,
        }

        if val is None and (str_types.get(field.type) is None or not field.required):
            continue

        if not isinstance(val, str_types.get(field.type)):  # type: ignore
            raise ValueError(
                f"Field `{field_name}`: Expected type {field.type} but got {type(val)}"
            )

        payload[field.name] = val

    return payload


def save_document(
    fs_doc: firestore_types.DocumentReference, payload: dict[str, Any]
) -> firestore_types.DocumentReference:
    """Save a document to firestore. Fields are unvalidated.

    Args:
        fs_doc: The firestore document.
        payload: The document payload.

    Returns:
        The firestore document.
    """
    fs_doc.set(payload)
    return fs_doc


def save_validated_document(
    fs_doc: firestore_types.DocumentReference,
    fields: dict[str, DocField],
    payload: dict[str, Any],
) -> firestore_types.DocumentReference:
    """Save a document to firestore. Fields are validated.

    Args:
        fs_doc: The firestore document.
        fields: The document fields.
        payload: The document payload.

    Returns:
        The firestore document.
    """
    payload = validate_document(fields, payload)
    return save_document(fs_doc, payload)


def save_document_from_template(
    engine: firestore_types.Client,
    path: str,
    instance: DocTemplateInstance,
) -> firestore_types.DocumentReference:
    """Save a document to firestore.

    Args:
        engine: The database engine.
        path: The document path. (e.g. "mining/datasource/raw_data/2340923741209")
        instance: The document instance.

    Returns:
        The firestore document.
    """
    doc_template = resolve_document_template_from_path(engine, path)
    fs_doc: firestore_types.DocumentReference = resolve_document_from_path(engine, path)
    return save_validated_document(fs_doc, doc_template.fields, instance.values)


def read_document(
    fs_doc: firestore_types.DocumentReference,
) -> firestore_types.DocumentSnapshot:
    """Read a document from firestore.

    Args:
        fs_doc: The firestore document.

    Returns:
        The document payload.
    """
    return fs_doc.get()


def read_document_from_path(
    engine: firestore_types.Client, path: str
) -> firestore_types.DocumentSnapshot:
    """Read a document from firestore.

    Args:
        engine: The database engine.
        path: The document path. (e.g. "mining/datasource/raw_data/2340923741209")

    Returns:
        The document payload.
    """
    resolve_document_template_from_path(engine, path)
    fs_doc: firestore_types.DocumentReference = resolve_document_from_path(engine, path)
    return read_document(fs_doc)


def filter_documents_from_path(
    engine: firestore_types.Client, path: str, filter_name: str, value: str
) -> list[firestore_types.DocumentSnapshot]:
    """Filter a collection from firestore.

    Args:
        engine: The database engine.
        path: The document path. (e.g. "mining/datasource/raw_data")
        filter_name: name of field that you want to filter accordingly (e.g. company_id)
        value: Actual value for the filter

    Returns:
        List of documents
    """
    current_collection = _resolve_from_path(engine, path, False)
    return current_collection.where(
        filter=firestore_types.FieldFilter(filter_name, "==", value)
    ).get()


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
