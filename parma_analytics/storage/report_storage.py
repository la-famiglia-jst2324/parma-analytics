import os
from datetime import timedelta
from typing import Any

from firebase_admin import storage
from google.cloud.storage import Blob

from parma_analytics.vendor.firebase import get_app


class FirebaseStorageManager:
    def __init__(self) -> None:
        self.app = get_app()
        self.bucket = storage.bucket()

    def add_company_file(self, company_id: str, file_path: str) -> Blob:
        blob_path = f"reports/companies/{company_id}/{os.path.basename(file_path)}"
        return self._upload_file(blob_path, file_path)

    def add_user_file(self, user_id: str, file_path: str) -> Blob:
        blob_path = f"reports/users/{user_id}/{os.path.basename(file_path)}"
        return self._upload_file(blob_path, file_path)

    def _upload_file(self, blob_path: str, file_path: str) -> Blob:
        blob = self.bucket.blob(blob_path)
        blob.upload_from_filename(file_path)
        return blob

    def get_file_path(self, blob: Blob) -> str:
        return blob.path

    def get_existing_blob(self, file_path: str) -> Blob | None:
        blob = self.bucket.blob(file_path)
        if blob.exists():
            return blob
        else:
            return None

    def get_download_url(self, blob: Blob) -> str:
        return blob.generate_signed_url(
            timedelta(days=1)
        )  # Time can be changed, depending on the use case

    def get_file_metadata(self, blob: Blob) -> dict[str, Any]:
        blob.reload()
        return {
            "name": blob.name,
            "created_at": blob.time_created,
            "size": blob.size,
            "content_type": blob.content_type,
            "path": blob.path,
            "download_url": blob.generate_signed_url(
                timedelta(days=1)
            ),  # Time can be changed, depending on the use case
        }
