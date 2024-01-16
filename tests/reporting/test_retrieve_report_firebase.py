import unittest
from unittest.mock import Mock, patch

from parma_analytics.reporting.retrieve_report_firebase import retrieve_reports


class TestRetrieveReports(unittest.TestCase):
    """Test case for Retrieving Reports."""

    @patch("parma_analytics.reporting.retrieve_report_firebase.FirebaseStorageManager")
    def test_retrieve_reports(self, mock_firebase_storage_manager):
        """Function to test retrireve reports."""
        user_id = "test_user"
        mock_storage_manager_instance = mock_firebase_storage_manager.return_value

        mock_blob1 = Mock(name="blob1")
        mock_blob1.name = "reports/users/test_user/report_20240115000001.pdf"

        mock_blob2 = Mock(name="blob2")
        mock_blob2.name = "reports/users/test_user/report_20240114000012.pdf"

        mock_storage_manager_instance.get_existing_blobs.return_value = [
            mock_blob2,
            mock_blob1,
        ]

        mock_storage_manager_instance.get_download_url.return_value = "mocked_url"
        result = retrieve_reports(user_id)

        mock_storage_manager_instance.get_existing_blobs.assert_called_once_with(
            "reports/users/test_user/"
        )
        self.assertEqual(result, "mocked_url")
