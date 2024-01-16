"""Retrieving the reports from FireBase."""

from datetime import datetime, timedelta

from parma_analytics.storage.report_storage import FirebaseStorageManager


def retrieve_reports(user_id: str):
    """Retrieve the reports for a user and send it via email."""
    firebase_storage_manager = FirebaseStorageManager()
    user_folder_path = f"reports/users/{user_id}/"
    blobs = firebase_storage_manager.get_existing_blobs(user_folder_path)
    latest_report = None
    latest_timestamp = 0
    one_week_ago = datetime.now() - timedelta(days=7)
    one_week_ago_timestamp = int(one_week_ago.strftime("%Y%m%d%H%M%S"))
    if blobs is not None:
        for blob in blobs:
            timestamp_str = (
                blob.name.replace(user_folder_path, "")
                .replace("report_", "")
                .replace(".pdf", "")
            )

            try:
                timestamp = int(timestamp_str)
            except ValueError:
                continue
            if timestamp > latest_timestamp and timestamp > one_week_ago_timestamp:
                latest_timestamp = timestamp
                latest_report = blob

        if latest_report is not None:
            return firebase_storage_manager.get_download_url(blob)
