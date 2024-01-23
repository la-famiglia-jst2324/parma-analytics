import os
from datetime import timedelta

import pytest

from parma_analytics.storage.report_storage import FirebaseStorageManager

manager = FirebaseStorageManager()


def test_add_company_file(tmpdir):
    file_path = str(tmpdir.join("test_file.txt"))
    with open(file_path, "w") as f:
        f.write("This is a test file.")

    company_id = "acme"
    blob = manager.add_company_file(company_id, file_path)

    assert blob.exists()
    assert blob.name == "reports/companies/acme/test_file.txt"


def test_add_user_file(tmpdir):
    file_path = str(tmpdir.join("test_file.txt"))
    with open(file_path, "w") as f:
        f.write("This is a test file.")

    user_id = "johndoe"

    manager = FirebaseStorageManager()
    blob = manager.add_user_file(user_id, file_path)
    print(blob.path)
    assert blob.exists()
    assert blob.name == "reports/users/johndoe/test_file.txt"


@pytest.fixture
def blob(tmpdir):  # Add tmpdir as a parameter
    manager = FirebaseStorageManager()
    # Upload a test file to the storage bucket
    file_path = str(tmpdir.join("test_file.txt"))
    with open(file_path, "w") as f:
        f.write("This is a test file.")
    blob = manager.add_company_file("acme", file_path)
    return blob


def test_get_file_path(blob):
    expected_path = "reports/companies/acme/test_file.txt"
    expected_path = expected_path.replace("/", "%2F")
    assert manager.get_file_path(blob).endswith(expected_path)
    assert manager.get_file_path(blob).startswith(
        "/b/la-famiglia-parma-ai-staging.appspot.com/"
    )


def test_get_existing_blob(tmpdir):
    file_path = str(tmpdir.join("test_file.txt"))
    with open(file_path, "w") as f:
        f.write("This is a test file.")
    blob = manager.add_company_file("test1", file_path)
    print(blob.name)
    print(blob.generation)
    print(blob)
    existing_blob = manager.get_existing_blob(blob.name)
    assert existing_blob is not None
    assert existing_blob.name == blob.name
    assert existing_blob.path == blob.path
    blob.delete()
    none_blob = manager.get_existing_blob(blob.name)
    assert none_blob is None


def test_get_download_url(blob):
    validity = timedelta(days=1)
    signed_url = manager.get_download_url(blob, validity)
    assert signed_url.startswith(
        "https://storage.googleapis.com/la-famiglia-parma-ai-staging.appspot.com/reports/companies/acme/test_file.txt"
    )


def test_get_file_metadata(blob, tmpdir):
    metadata = manager.get_file_metadata(blob)
    assert metadata.get("name") == "reports/companies/acme/test_file.txt"
    assert metadata.get("created_at") is not None
    assert metadata.get("size") == os.path.getsize(str(tmpdir.join("test_file.txt")))
    assert metadata.get("content_type") == "text/plain"
    if (path := metadata.get("path")) is not None:
        assert path.endswith("reports%2Fcompanies%2Facme%2Ftest_file.txt")
    else:
        assert False
    assert metadata.get("download_url")
