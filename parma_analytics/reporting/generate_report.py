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
            return response.choices[0].text

        except Exception as e:
            logging.error(f"An error occurred while calling GPT: {e}")
            raise e

    def generate_report(self, report_params) -> dict:
        """Generates the report content using GPT.

        Args:
            report_params: An object containing information to generate a  prompt

        Returns:
            str: A summary string containing information about the
                report, including trigger change,
                current value, metric name, timeframe, etc.
        """
        try:
            company_name = report_params["company_name"]
            source_name = report_params["source_name"]
            timeframe = report_params["timeframe"]
            metric_name = report_params["metric_name"]
            trigger_change = report_params["trigger_change"]
            current_value = report_params["current_value"]
            previous_value = report_params["previous_value"]
            aggregated_method = report_params["aggregated_method"]
            if not aggregated_method:
                with open(
                    "parma_analytics/reporting/prompts/summary_generator.txt"
                ) as prompt_file:
                    prompt = f"{prompt_file.read()}"

                gpt_prompt = prompt.format(
                    company_name=company_name,
                    timeframe=timeframe,
                    source_name=source_name,
                    metric_name=metric_name,
                    trigger_change=trigger_change,
                    current_value=current_value,
                )
            else:
                with open(
                    "parma_analytics/reporting/prompts/aggregated_data_summary.txt"
                ) as prompt_file:
                    prompt = f"{prompt_file.read()}"

                gpt_prompt = prompt.format(
                    company_name=company_name,
                    source_name=source_name,
                    metric_name=metric_name,
                    trigger_change=trigger_change,
                    current_value=current_value,
                    previous_value=previous_value,
                    aggregated_method=aggregated_method,
                )

            with open(
                "parma_analytics/reporting/prompts/title_prompt.txt"
            ) as prompt_file:
                prompt = f"{prompt_file.read()}"

            title_gpt_prompt = prompt.format(
                company_name=company_name,
                metric_name=metric_name,
                trigger_change=trigger_change,
            )
            print(gpt_prompt)
            summary = self._make_openai_request(gpt_prompt)
            title = self._make_openai_request(title_gpt_prompt)
            return {"title": title, "summary": summary}
        except Exception as e:
            logging.error(f"An error occurred in reporting/generate_report: {e}")
            raise e
