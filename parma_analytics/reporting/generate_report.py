"""Generates the report for the companies and sends it to them via email."""

from datetime import datetime

from generate_html import generate_html_report
from generate_pdf import generate_pdf

from parma_analytics.bl.generate_report import generate_report
from parma_analytics.storage.report_storage import FirebaseStorageManager


def generate_reports(user_id) -> None:
    """Generates the report for the companies and sends it to them via email."""
    df, measurement_data = generate_report()
    grouped_data = {}
    for row in df.iter_rows():
        (
            company_measurement_id,
            company_id,
            company_description,
            company_name,
            source_module_id,
            source_name,
            measurement_id,
            measurement_name,
            measurement_type,
        ) = row

        if company_id not in grouped_data:
            grouped_data[company_id] = {
                "company_name": company_name,
                "company_description": company_description,
                "sources": {},
            }

        if source_module_id not in grouped_data[company_id]["sources"]:
            grouped_data[company_id]["sources"][source_module_id] = {
                "source_name": source_name,
                "measurements": [],
            }

        grouped_data[company_id]["sources"][source_module_id]["measurements"].append(
            {
                "measurement_id": measurement_id,
                "measurement_name": measurement_name,
                "measurement_type": measurement_type,
                "company_measurement_id": company_measurement_id,
            }
        )

    grouped_data_list = list(grouped_data.values())

    html_content = generate_html_report(grouped_data_list, measurement_data)
    pdf = generate_pdf(html_content)
    firebase_storage_manager = FirebaseStorageManager()
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f"report_{timestamp}.pdf"
    content_type = "application/pdf"
    firebase_storage_manager.upload_string_to_user(
        user_id, pdf, file_name, content_type
    )
    firebase_storage_manager.get_existing_blobs("549")
