import unittest
from unittest.mock import patch

from parma_analytics.bl.fetch_crm_companies import get_new_crm_companies_bll


class TestGetNewCrmCompaniesBll(unittest.TestCase):
    """Test class."""

    @patch("parma_analytics.db.prod.company_query.get_session")
    @patch("parma_analytics.db.prod.company_query.company_exists_by_name")
    @patch("parma_analytics.db.prod.company_query.create_company")
    def test_no_new_companies(
        self, mock_create_company, mock_company_exists_by_name, mock_get_session
    ):
        """Test no new companies."""
        # Arrange
        user_id = 1
        mock_get_session.return_value.__enter__.return_value = None
        mock_company_exists_by_name.return_value = True
        mock_create_company.return_value = None

        # Act
        result = get_new_crm_companies_bll(user_id)

        # Assert
        self.assertEqual(result, "No new companies found in the CRM")


if __name__ == "__main__":
    unittest.main()
