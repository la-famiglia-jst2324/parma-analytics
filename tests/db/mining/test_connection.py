from firebase_admin.firestore import firestore as firestore_types


def test_get_engine(engine: firestore_types.Client):
    assert engine is not None

    # create test document in test collection
    test_collection = engine.collection("test")
    test_document = test_collection.document("test")
    test_document.set({"test": "test"})
    assert engine.collection("test").document("test").get().to_dict() == {
        "test": "test"
    }

    # cleanup
    engine.collection("test").document("test").delete()
