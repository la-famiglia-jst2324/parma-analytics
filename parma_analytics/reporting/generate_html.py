from jinja2 import Environment, FileSystemLoader
from generate_charts import generate_chart
import pandas as pd


def generate_html_report(
    data_frame,
    int_measurement_data,
    float_measurement_data,
    comment_measurement_data,
    text_measurement_data,
    paragraph_measurement_data,
):
    env = Environment(loader=FileSystemLoader("parma_analytics/reporting"))
    template = env.get_template("report_template.html")

    html_content = template.render(
        data_frame=data_frame,
        int_measurement_data=int_measurement_data,
        float_measurement_data=float_measurement_data,
        comment_measurement_data=comment_measurement_data,
        text_measurement_data=text_measurement_data,
        paragraph_measurement_data=paragraph_measurement_data,
        generate_chart=generate_chart,
        get_value_for_measurement=get_value_for_measurement,
    )

    html_file_path = "data_analysis_report.html"
    with open(html_file_path, "w") as html_file:
        html_file.write(html_content)

    return html_content


def get_value_for_measurement(
    company_measurement_id, comment_data_frame, text_data_frame, paragraph_data_frame
):
    data_frames = [comment_data_frame, text_data_frame, paragraph_data_frame]

    filtered_data_frames = []
    for df in data_frames:
        if not df.empty:
            filtered_df = df[df["company_measurement_id"] == company_measurement_id]
            filtered_data_frames.append(filtered_df)

    concatenated_df = pd.concat(filtered_data_frames, ignore_index=True)

    if concatenated_df.empty:
        return None

    recent_value = concatenated_df["value"].max()
    return recent_value
