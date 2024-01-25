import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

from parma_analytics.bl.generate_report import (
    GenerateReportInput,
    generate_report,
)


class TestReportGenerator(unittest.TestCase):
    """Test case for generating report summary and title by GPT."""

    def test_generate_report(self):
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
            mock_engine = MagicMock()
            mock_get_engine.return_value = mock_engine
            mock_get_company_name.return_value = "ABC Corp"
            mock_source_module = MagicMock()
            mock_source_module.type = "SALES"
            mock_get_source_measurement_query.return_value = mock_source_module
            mock_get_data_source_name.return_value = "Sales Source"
            mock_fetch_recent_value.return_value = {"timestamp": datetime.now()}

            input_params = GenerateReportInput(
                company_id=1,
                source_measurement_id=1,
                company_measurement_id=1,
                current_value=1000,
                trigger_change=2,
                previous_value=800,
                aggregation_method="sum",
                type="int",
            )

            mock_report_generator_instance = MagicMock()
            mock_report_generator.return_value = mock_report_generator_instance
            mock_report_generator_instance.generate_report.return_value = {
                "title": "Report Title",
                "summary": "Report Summary",
            }

            result = generate_report(input_params)

            self.assertIsInstance(result, dict)
            self.assertIn("title", result)
            self.assertIn("summary", result)

            mock_get_engine.assert_called_once()
            mock_get_company_name.assert_called_once_with(mock_engine, 1)
            mock_get_source_measurement_query.assert_called_once_with(mock_engine, 1)
            mock_get_data_source_name.assert_called_once_with(
                mock_engine, mock_source_module.source_module_id
            )
            mock_fetch_recent_value.assert_called_once_with(
                mock_engine, 1, "measurement_sales_value"
            )
            mock_report_generator.assert_called_once()
            mock_report_generator_instance.generate_report.assert_called_once_with(
                {
                    "company_name": "ABC Corp",
                    "source_name": "Sales Source",
                    "metric_name": mock_get_source_measurement_query().measurement_name,
                    "trigger_change": 2.0,
                    "previous_value": 800,
                    "current_value": 1000,
                    "timeframe": 0,
                    "aggregated_method": "sum",
                    "type": "int",
                }
            )
