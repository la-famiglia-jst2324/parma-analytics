import os
from pathlib import Path
from unittest import mock

import pytest

from parma_analytics.utils.uuid import generate_uuid
from parma_analytics.vendor.gcp import CREDENTIALS_PATH, get_credentials


def test_get_credentials(tmp_path_factory, monkeypatch):
    assert os.environ.get("GCP_SECRET_MANAGER_CERTIFICATE") or CREDENTIALS_PATH.exists()

    # Test with env var
    if os.environ.get("GCP_SECRET_MANAGER_CERTIFICATE"):
        assert get_credentials() is not None

    else:
        with mock.patch.dict(
            os.environ, {"GCP_SECRET_MANAGER_CERTIFICATE": CREDENTIALS_PATH.read_text()}
        ):
            assert get_credentials() is not None

    # test with file
    gcp_secret = os.environ.get("GCP_SECRET_MANAGER_CERTIFICATE")
    with mock.patch.dict(
        os.environ,
        {k: v for k, v in os.environ.items() if k != "GCP_SECRET_MANAGER_CERTIFICATE"},
        clear=True,
    ):
        if not CREDENTIALS_PATH.exists():
            tmp_path = tmp_path_factory.mktemp(
                f"tmpfile-gcp-secrets-{generate_uuid()}.json", numbered=False
            )
            tmp_path.write_text(gcp_secret)
            monkeypatch.setattr(
                "parma_analytics.vendor.gcp.CREDENTIALS_PATH", tmp_path.absolute()
            )
            assert get_credentials() is not None
        else:
            assert get_credentials() is not None


def test_get_credentials_fail(monkeypatch):
    with mock.patch.dict(
        os.environ,
        {k: v for k, v in os.environ.items() if k != "GCP_SECRET_MANAGER_CERTIFICATE"},
        clear=True,
    ):
        not_existing = Path(__file__) / "not_found.json"
        monkeypatch.setattr("parma_analytics.vendor.gcp.CREDENTIALS_PATH", not_existing)
        with pytest.raises(FileNotFoundError):
            get_credentials()
