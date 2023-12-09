from typing import cast

from firebase_admin.firestore import firestore as firestore_types


def test_collections(engine: firestore_types.Client):
    collections = engine.collections()
    typed_collections = [
        cast(firestore_types.CollectionReference, c) for c in collections
    ]
    collection_ids = [c.id for c in typed_collections]

    assert "parma" in collection_ids


def test_param_collection_docs(engine: firestore_types.Client):
    parma_collection = engine.collection("parma")
    documents = parma_collection.list_documents()
    typed_docs = [cast(firestore_types.DocumentReference, d) for d in documents]
    doc_ids = [d.id for d in typed_docs]

    assert "mining" in doc_ids
    assert "analytics" in doc_ids
    assert "frontend" in doc_ids


def test_parma_mining_datasource_docs(engine: firestore_types.Client):
    datasource_collection: firestore_types.CollectionReference = (
        engine.collection("parma").document("mining").collection("datasource")
    )
    assert datasource_collection

    for d in datasource_collection.list_documents():
        doc_datasource = cast(firestore_types.DocumentReference, d)
        content = doc_datasource.get()
        assert content.exists

        # for every datasource doc, check it's contents
        sub_collections = doc_datasource.collections()
        typed_sub_collection = [
            cast(firestore_types.DocumentReference, c) for c in sub_collections
        ]
        [c.id for c in typed_sub_collection]

        # assert raw_data contents
        raw_data_collection = doc_datasource.collection("raw_data")
        for raw_data_doc in cast(
            firestore_types.CollectionReference, raw_data_collection
        ).list_documents():
            typed_raw_data_doc = cast(firestore_types.DocumentReference, raw_data_doc)
            content = typed_raw_data_doc.get()
            assert content.exists
            assert (
                len({"mining_trigger", "status", "data"} - content.to_dict().keys())
                == 0
            )

        # assert normalization_schema contents
        normalization_schema_collection = doc_datasource.collection(
            "normalization_schema"
        )
        for normalization_schema_doc in cast(
            firestore_types.CollectionReference, normalization_schema_collection
        ).list_documents():
            typed_normalization_schema_doc = cast(
                firestore_types.DocumentReference, normalization_schema_doc
            )
            content = typed_normalization_schema_doc.get()
            assert content.exists
            assert len({"schema"} - content.to_dict().keys()) == 0


def test_parma_mining_trigger_docs(engine: firestore_types.Client):
    trigger_collection: firestore_types.CollectionReference = (
        engine.collection("parma").document("mining").collection("trigger")
    )
    assert trigger_collection

    for d in trigger_collection.list_documents():
        doc_trigger = cast(firestore_types.DocumentReference, d)
        content = doc_trigger.get()
        assert content.exists

        # for every trigger doc, check it's contents
        assert (
            len(
                {
                    "datasource",
                    "started_at",
                    "finished_at",
                    "scheduled_task_id",
                    "status",
                }
                - content.to_dict().keys()
            )
            == 0
        )
