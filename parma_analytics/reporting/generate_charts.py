"""Contains functions for generating charts from measurement data."""

import base64
from io import BytesIO
from typing import Any

import matplotlib.pyplot as plt
from matplotlib import font_manager

primary_color = "#111828"
secondary_color = "#1A1A24"
background_color = "#1a1a1a"

font_path = "parma_analytics/reporting/report_template/static/Inter-Regular.ttf"
font_manager.fontManager.addfont(font_path)


def generate_bar_chart(
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
    # if not value:
    #     return False

    plt.figure(figsize=(10, 6), facecolor=background_color)
    plt.bar(range(len(value)), value, color=primary_color)
    plt.title(f"Bar Chart for Company {company_name}", fontsize=20)
    plt.xlabel("Categories", fontsize=15)
    plt.ylabel(f"{measurement_name}", fontsize=15)
    plt.xticks(range(len(value)), fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()

    chart_data = base64.b64encode(buffer.read()).decode("utf-8")
    return chart_data


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
    # plt.style.use('seaborn-v0_8-dark')
    # plt.style.use('grayscale')
    value = measurement_data.filter(
        measurement_data["company_measurement_id"] == company_measurement_id
    )["value"].to_list()
    # if not value:
    #     return False
    font_properties = {
        "weight": "bold",
        "fontname": font_manager.FontProperties(fname=font_path).get_name(),
    }

    print(font_properties)

    plt.figure(figsize=(24, 10), facecolor=secondary_color)
    ax = plt.axes()
    ax.set_facecolor(primary_color)
    plt.plot(
        value, marker="o", markersize=12, linestyle="-", color="#a49d9d"
    )  # Adjust marker size

    # Customize title and axis labels
    plt.title(
        f"Change Over Time for Company {company_name}",
        fontsize=30,
        color="white",
        **font_properties,
    )
    plt.xlabel("Timestamp", fontsize=30, color="white", **font_properties)
    plt.ylabel(f"{measurement_name}", fontsize=30, color="white", **font_properties)

    # Customize tick labels
    plt.xticks(range(len(value)), fontsize=20, color="gray", **font_properties)
    plt.yticks(fontsize=20, color="gray", **font_properties)

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()

    chart_data = base64.b64encode(buffer.read()).decode("utf-8")
    return chart_data
