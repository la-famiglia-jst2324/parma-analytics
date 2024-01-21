"""Generates the report for the companies using GPT."""

import logging
import os

from openai import OpenAI


class ReportGenerator:
    """Class to generate reports."""

    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)

    def _make_openai_request(self, prompt):
        """Make a request to the OpenAI API.

        Args:
            prompt (str): The prompt to be used in the API request.

        Returns:
            dict: The response from the OpenAI API.
        """
        try:
            response = self.client.completions.create(
                prompt=prompt, model="gpt-3.5-turbo-instruct", max_tokens=200
            )
            return response

        except Exception as e:
            logging.error(f"An error occurred while calling GPT: {e}")
            raise e

    def generate_report_summary(self, report_params) -> str:
        """Generates the report content using GPT.

        Args:
            report_params: An object containing information to generate a  prompt

        Returns:
            str: A summary string containing information about the
                report, including trigger change,
                current value, metric name, timeframe, etc.
        """
        company_name = report_params["company_name"]
        source_name = report_params["source_name"]
        timeframe = report_params["timeframe"]
        metric_name = report_params["metric_name"]
        trigger_change = report_params["trigger_change"]
        current_value = report_params["current_value"]
        gpt_prompt = f"""I want you to act as a summary generator. Generate a
                     concise 1-2 linesexpressive summary for a
                     company {company_name} who recently witnessed a change
                     within the {timeframe} days on the {source_name}platform
                     for {metric_name}  of {trigger_change}  %  and its current
                     value of is now {current_value}. Adjust the timeframe
                     representation to yeasrs if days > 365 or months if
                     days > 28 if necessary or weeks if days > 7"""

        response = self._make_openai_request(gpt_prompt)
        return response.choices[0].text
