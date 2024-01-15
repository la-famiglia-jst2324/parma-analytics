"""Generates an HTML report from a template and data."""

import polars as pl
from generate_charts import generate_chart
from jinja2 import Environment, FileSystemLoader


def generate_html_report(data_for_template, measurement_data) -> str:
    """Generate an HTML report from a template and data.

    Args:
        data_for_template: data for the template.
        measurement_data: measurement data.

    Returns:
        An HTML report.
    """
    env = Environment(loader=FileSystemLoader("parma_analytics/reporting"))
    template = env.get_template("report_template/report_template.html")

    template_context = {
        "data_for_template": data_for_template,
        "generate_chart": generate_chart,
        "get_value_for_measurement": get_value_for_measurement,
        "int_measurement_data": measurement_data.get("Int", pl.DataFrame()),
        "float_measurement_data": measurement_data.get("Float", pl.DataFrame()),
        "comment_measurement_data": measurement_data.get("Comment", pl.DataFrame()),
        "text_measurement_data": measurement_data.get("Text", pl.DataFrame()),
        "paragraph_measurement_data": measurement_data.get("Paragraph", pl.DataFrame()),
    }

    html_content = template.render(**template_context)
    # with open("some Path.html", "w") as html_file:
    #     html_file.write(html_content)

    return html_content


def get_value_for_measurement(company_measurement_id: int, data_frame: pl.DataFrame):
    """Get the value for a measurement.

    Args:
        company_measurement_id: id of the measurement.
        data_frame: measurement data.

    Returns:
        The value of the measurement.
    """
    filtered_df = data_frame.filter(
        data_frame["company_measurement_id"] == company_measurement_id
    )

    sorted_df = filtered_df.sort("created_at", descending=True)
    if sorted_df.shape[0] == 0:
        return False

    most_recent_value = sorted_df.select("value").head(1)["value"][0]

    return most_recent_value
