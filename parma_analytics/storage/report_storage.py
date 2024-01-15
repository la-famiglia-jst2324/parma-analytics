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

    def get_existing_blobs(self, folder_path: str) -> Blob | None:
        """Retrieve existing blobs (files) in the specified user's folder.

        Args:
            folder_path: The folder path.

        Returns:
            The list of blobs
        """
        blobs = self.bucket.list_blobs(prefix=folder_path)
        return blobs

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

    def upload_string_to_user(
        self, user_id: str, file_content: str, file_name: str, content_type: str
    ) -> str:
        """Upload a file content as string to the user's folder.

        Args:
            user_id: The id of the user.
            file_content: The content of the file to upload as a string.
            file_name: The name of the file.
            content_type: The type of file to upload

        Returns:
            The uploaded file.
        """
        blob_path = f"reports/users/{user_id}/{file_name}"
        return self._upload_string(blob_path, file_content, content_type)

    # ----------------------------------- Internal ----------------------------------- #

    def _upload_file(self, blob_path: str, file_path: str) -> Blob:
        blob = self.bucket.blob(blob_path)
        blob.upload_from_filename(file_path)
        return blob

    def _upload_string(
        self, blob_path: str, file_content: str, content_type: str
    ) -> str:
        """Upload a file content as string to Firebase Cloud Storage.

        Args:
            blob_path: The destination path for the file in the storage bucket.
            file_content: The content of the file to upload as a string.
            content_type: The type of file to upload

        Returns:
            The uploaded file.
        """
        blob = self.bucket.blob(blob_path)
        blob.upload_from_string(file_content, content_type)
        return blob
