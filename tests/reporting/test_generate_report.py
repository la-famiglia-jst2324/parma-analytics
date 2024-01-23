import unittest

from parma_analytics.reporting.generate_report import ReportGenerator


class TestReportGenerator(unittest.TestCase):
    """Test case for generating report summary and title by GPT."""

    def test_generate_report(self):
        """Report test."""
        report_generator = ReportGenerator()

        report_params_1 = {
            "company_name": "ABC Corp",
            "source_name": "Linkedin",
            "timeframe": 10,
            "metric_name": "Revenue",
            "trigger_change": 5.0,
            "current_value": 1000000,
            "previous_value": 800000,
            "aggregated_method": "sum",
        }

        result_1 = report_generator.generate_report(report_params_1)
        self.assertIsInstance(result_1, dict)
        self.assertIn("title", result_1)
        self.assertIn("summary", result_1)

        report_params_2 = {
            "company_name": "XYZ Inc",
            "source_name": "ProductHunt",
            "timeframe": 20,
            "metric_name": "Customer Acquisition Cost",
            "trigger_change": 10.0,
            "current_value": 500,
            "previous_value": None,
            "aggregated_method": None,
        }

        result_2 = report_generator.generate_report(report_params_2)

        self.assertIsInstance(result_2, dict)
        self.assertIn("title", result_2)
        self.assertIn("summary", result_2)
