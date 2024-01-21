import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

from sqlalchemy.engine.base import Engine

from parma_analytics.bl.generate_report import (
    generate_report,
)


class TestGenerateReport(unittest.TestCase):
    """Test cases when generating report summaries."""

    def test_generate_report_successful(self):
        """Test the successful generation of a report."""
        with patch(
            "parma_analytics.bl.generate_report.ReportGenerator"
        ) as mock_report_generator, patch(
            "parma_analytics.bl.generate_report.fetch_recent_value"
        ) as mock_fetch_recent_value, patch(
            "parma_analytics.bl.generate_report.get_data_source_name"
        ) as mock_get_data_source_name, patch(
            "parma_analytics.bl.generate_report.get_source_measurement_query"
        ) as mock_get_source_measurement_query, patch(
            "parma_analytics.bl.generate_report.get_engine"
        ) as mock_get_engine, patch(
            "parma_analytics.bl.generate_report.get_company_name"
        ) as mock_get_company_name:
            company_id = 1
            source_measurement_id = 2
            company_measurement_id = 3
            current_value = 42.0
            trigger_change = 5.0

            mock_engine_instance = MagicMock(spec=Engine)
            mock_get_engine.return_value = mock_engine_instance

            mock_company_name = "Company x"
            mock_get_company_name.return_value = mock_company_name

            mock_source_measurement_query = MagicMock()
            mock_get_source_measurement_query.return_value = (
                mock_source_measurement_query
            )

            mock_data_source_name = "Linkedin"
            mock_get_data_source_name.return_value = mock_data_source_name

            mock_recent_value = {"value": 123.45, "timestamp": datetime.now()}
            mock_fetch_recent_value.return_value = mock_recent_value

            mock_report_generator_instance = MagicMock()
            mock_report_generator.return_value = mock_report_generator_instance
            summary_return = """A short summary of company x from
                                linkedin with 5% change and current value is 123.45"""
            mock_report_generator_instance.generate_report_summary.return_value = (
                summary_return
            )

            summary = generate_report(
                company_id,
                source_measurement_id,
                company_measurement_id,
                current_value,
                trigger_change,
            )

            mock_get_company_name.assert_called_once_with(
                mock_engine_instance, company_id
            )
            mock_get_source_measurement_query.assert_called_once_with(
                mock_engine_instance, source_measurement_id
            )
            mock_get_data_source_name.assert_called_once_with(
                mock_engine_instance, mock_source_measurement_query.source_module_id
            )
            mock_fetch_recent_value.assert_called_once_with(
                mock_engine_instance,
                company_measurement_id,
                f"measurement_{mock_source_measurement_query.type.lower()}_value",
            )

            mock_report_generator_instance.generate_report_summary.assert_called_once_with(
                {
                    "company_name": mock_company_name,
                    "source_name": mock_data_source_name,
                    "trigger_change": trigger_change * 100,
                    "current_value": current_value,
                    "metric_name": mock_source_measurement_query.measurement_name,
                    "timeframe": 0,
                }
            )

            self.assertEqual(summary, summary_return)
