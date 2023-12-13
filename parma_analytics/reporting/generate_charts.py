import base64
from io import BytesIO

import matplotlib.pyplot as plt
import pandas as pd


def generate_chart(
    df, measurement_data, company_id, source_module_id, company_measurement_id
):
    filtered_df = df[
        (df["company_id"] == company_id)
        & (df["source_module_id"] == source_module_id)
        & (df["company_measurement_id"] == company_measurement_id)
    ]
    merged_df = pd.merge(
        filtered_df,
        measurement_data[["company_measurement_id", "value", "created_at"]],
        on="company_measurement_id",
        how="left",
    )
    if merged_df["value"].isnull().any():
        return False
    company_name = df.loc[df["company_id"] == company_id, "company_name"].iloc[0]
    measurement_name = df.loc[
        df["company_measurement_id"] == company_measurement_id, "measurement_name"
    ].iloc[0]
    plt.figure(figsize=(10, 6))
    plt.plot(
        merged_df["created_at"],
        merged_df["value"],
        marker="o",
        linestyle="-",
        color="b",
    )
    plt.title(f"{measurement_name} Change Over Time for Company {company_name}")
    plt.xlabel("Timestamp")
    plt.ylabel(measurement_name)
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()

    chart_data = base64.b64encode(buffer.read()).decode("utf-8")

    return f"data:image/png;base64,{chart_data}"
