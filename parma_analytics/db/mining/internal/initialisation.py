"""Firestore schema initialisation utilities.

Checkout the README for more information on the nosql database schema.
"""


from firebase_admin.firestore import firestore as firestore_types

from parma_analytics.db.mining.internal.storage import save_validated_document

from ..engine import get_engine
from .definitions import parma_collection
from .models import (
    Collection,
    Doc,
    DocTemplate,
    DocTemplateInstance,
)


def init_schema() -> None:
    """Initialize the database schema."""
    engine = get_engine()

    assert isinstance(
        parma_collection.docs["mining"].collections["datasource"].docs, DocTemplate
    )
    for datasource in ["github", "reddit", "affinity"]:  # TODO: use db
        parma_collection.docs["mining"].collections["datasource"].docs.instances[
            datasource
        ] = DocTemplateInstance(name=datasource)

    # traversal algorithm (depth first)
    _traverse(engine, current_ref=None, current_item=parma_collection)


# ------------------------------------------------------------------------------------ #
#                                       Internal                                       #
# ------------------------------------------------------------------------------------ #

# ------------------------------------- Traversal ------------------------------------ #


def _traverse(
    engine: firestore_types.Client,
    current_ref: firestore_types.CollectionReference
    | firestore_types.DocumentReference
    | None,
    current_item: Collection | Doc | DocTemplate,
) -> None:
    """Traverse the schema tree and create the collections and docs.

    Args:
        path: The path to the parent item.
        current_item: The current item.
    """
    if isinstance(current_item, Collection):
        assert current_ref is None or isinstance(
            current_ref, firestore_types.DocumentReference
        )
        new_col = _create_collection(engine, current_ref, current_item)
        if isinstance(current_item.docs, dict):
            for doc_name, doc in current_item.docs.items():
                assert doc_name == doc.name
                _traverse(engine, new_col, doc)
        else:
            _traverse(engine, new_col, current_item.docs)

    elif isinstance(current_item, Doc):
        assert current_ref is None or isinstance(
            current_ref, firestore_types.CollectionReference
        )
        new_doc = _create_doc(current_ref, current_item)
        for col_name, col in current_item.collections.items():
            assert col_name == col.name
            _traverse(engine, new_doc, col)

    elif isinstance(current_item, DocTemplate):
        assert current_ref is None or isinstance(
            current_ref, firestore_types.CollectionReference
        )
        for doc_instance_name, doc_instance in current_item.instances.items():
            assert doc_instance_name == doc_instance.name
            new_doc = _create_doc_from_template(current_ref, current_item, doc_instance)
            if new_doc is None:
                continue
            for col_name, col in current_item.collections.items():
                assert col_name == col.name
                _traverse(engine, new_doc, col)

    else:
        raise ValueError(f"Unknown type: {type(current_item)}")


def _create_collection(
    engine: firestore_types.Client,
    parent_document: firestore_types.DocumentReference | None,
    collection: Collection,
) -> firestore_types.CollectionReference:
    if parent_document is None:
        return engine.collection(collection.name)
    return parent_document.collection(collection.name)


def _create_doc(
    parent_collection: firestore_types.CollectionReference, doc: Doc
) -> firestore_types.DocumentReference:
    fs_doc = parent_collection.document(doc.name)
    return save_validated_document(fs_doc, doc.fields, doc.values)


def _create_doc_from_template(
    parent_collection: firestore_types.CollectionReference,
    template: DocTemplate,
    instance: DocTemplateInstance,
) -> firestore_types.DocumentReference:
    # validate instances from template
    for field_name, field in template.fields.items():
        assert field_name == field.name
        value = instance.values.get(field.name)
        if value is None and field.required:
            raise ValueError(f"Required field {field.name} is missing.")

    fs_doc = parent_collection.document(instance.name)
    return save_validated_document(fs_doc, template.fields, instance.values)
