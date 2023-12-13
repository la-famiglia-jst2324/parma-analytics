from jinja2 import Environment, FileSystemLoader
from generate_charts import generate_chart


def generate_html_report(
    data_frame, int_measurement_data, float_measurement_data, comment_measurement_data
):
    env = Environment(loader=FileSystemLoader("parma_analytics/reporting"))
    template = env.get_template("report_template.html")

    html_content = template.render(
        data_frame=data_frame,
        int_measurement_data=int_measurement_data,
        float_measurement_data=float_measurement_data,
        comment_measurement_data=comment_measurement_data,
        generate_chart=generate_chart,
        get_value_for_measurement=get_value_for_measurement,
    )

    with open("data_analysis_report.html", "w") as html_file:
        html_file.write(html_content)


def get_value_for_measurement(company_measurement_id, comment_data_frame):
    if comment_data_frame.empty:
        return False

    filtered_df = comment_data_frame[
        comment_data_frame["company_measurement_id"] == company_measurement_id
    ]

    recent_value = filtered_df["value"].max() if not filtered_df.empty else None
    return recent_value
