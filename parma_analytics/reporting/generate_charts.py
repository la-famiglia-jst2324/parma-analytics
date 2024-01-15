"""Contains functions for generating charts from measurement data."""

import base64
from io import BytesIO
from typing import Any

import matplotlib.pyplot as plt


def generate_chart(
    measurement_data: Any,  # TODO: what is this?
    company_name: str,
    measurement_name: str,
    company_measurement_id: int,
) -> str:
    """Generate a chart from measurement data.

    Args:
        measurement_data: measurement data.
        company_name: name of the company.
        measurement_name: name of the measurement.
        company_measurement_id: id of the measurement.

    Returns:
        A base64 encoded png image.
    """
    value = measurement_data.filter(
        measurement_data["company_measurement_id"] == company_measurement_id
    )["value"].to_list()
    if not value:
        raise ValueError("No data found for the given company measurement id.")
    plt.figure(figsize=(10, 6))
    plt.plot(value, marker="o", linestyle="-", color="b")
    plt.title(f"Change Over Time for Company {company_name}")
    plt.xlabel("Timestamp")
    plt.ylabel(f"{measurement_name}")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()

    chart_data = base64.b64encode(buffer.read()).decode("utf-8")

    return f"data:image/png;base64,{chart_data}"
