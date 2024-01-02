"""Module for Firebase Storage operations."""

import os
from datetime import timedelta
from typing import Any

from firebase_admin import storage
from google.cloud.storage import Blob

from parma_analytics.vendor.firebase import get_app


class FirebaseStorageManager:
    """Manager for Firebase Storage operations."""

    def __init__(self) -> None:
        """Initialize the Firebase Storage Manager."""
        self.app = get_app()
        self.bucket = storage.bucket()

    def add_company_file(self, company_id: str, file_path: str) -> Blob:
        """Upload a file to the company's folder.

        Args:
            company_id: The id of the company.
            file_path: The path to the file to upload.

        Returns:
            The uploaded file.
        """
        blob_path = f"reports/companies/{company_id}/{os.path.basename(file_path)}"
        return self._upload_file(blob_path, file_path)

    def add_user_file(self, user_id: str, file_path: str) -> Blob:
        """Upload a file to the user's folder.

        Args:
            user_id: The id of the user.
            file_path: The path to the file to upload.

        Returns:
            The uploaded file.
        """
        blob_path = f"reports/users/{user_id}/{os.path.basename(file_path)}"
        return self._upload_file(blob_path, file_path)

    def get_file_path(self, blob: Blob) -> str:
        """Get the path of a file.

        Args:
            blob: Reference to the file.
        """
        return blob.path

    def get_existing_blob(self, file_path: str) -> Blob | None:
        """Get a reference to an existing file.

        Args:
            file_path: The path to the file.

        Returns:
            The file if it exists, None otherwise.
        """
        blob = self.bucket.blob(file_path)
        if blob.exists():
            return blob
        else:
            return None

    def get_download_url(
        self, blob: Blob, validity: timedelta = timedelta(days=1)
    ) -> str:
        """Generate a signed url for a file.

        Args:
            blob: Reference to the file.
            validity: How long the url will be valid.

        Returns:
            The signed url.
        """
        return blob.generate_signed_url(validity)

    def get_file_metadata(self, blob: Blob) -> dict[str, Any]:
        """Get the metadata of a file.

        Args:
            blob: Reference to the file.

        Returns:
            The metadata of the file.
        """
        blob.reload()
        return {
            "name": blob.name,
            "created_at": blob.time_created,
            "size": blob.size,
            "content_type": blob.content_type,
            "path": blob.path,
            "download_url": blob.generate_signed_url(timedelta(days=1)),
        }

    # ----------------------------------- Internal ----------------------------------- #

    def _upload_file(self, blob_path: str, file_path: str) -> Blob:
        blob = self.bucket.blob(blob_path)
        blob.upload_from_filename(file_path)
        return blob
