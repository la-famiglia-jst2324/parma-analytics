import polars as pl
from generate_charts import generate_chart
from jinja2 import Environment, FileSystemLoader


def generate_html_report(data_for_template, measurement_data):
    env = Environment(loader=FileSystemLoader("parma_analytics/reporting"))
    template = env.get_template("report_template.html")

    template_context = {
        "data_for_template": data_for_template,
        "generate_chart": generate_chart,
        "get_value_for_measurement": get_value_for_measurement,
        "int_measurement_data": measurement_data.get("int", pl.DataFrame()),
        "float_measurement_data": measurement_data.get("float", pl.DataFrame()),
        "comment_measurement_data": measurement_data.get("comment", pl.DataFrame()),
        "text_measurement_data": measurement_data.get("text", pl.DataFrame()),
        "paragraph_measurement_data": measurement_data.get("paragraph", pl.DataFrame()),
    }

    html_content = template.render(**template_context)
    html_file_path = "data_analysis_report.html"
    with open(html_file_path, "w") as html_file:
        html_file.write(html_content)

    return html_content


def get_value_for_measurement(company_measurement_id, data_frame):
    filtered_df = data_frame.filter(
        data_frame["company_measurement_id"] == company_measurement_id
    )

    sorted_df = filtered_df.sort("created_at")
    if sorted_df.shape[0] == 0:
        return False

    most_recent_value = sorted_df.select("value").head(1)["value"][0]

    return most_recent_value
