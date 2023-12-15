from parma_analytics.db.prod.report_data import fetch_data, fetch_measurement_data


def generate_report():
    df = fetch_data()
    measurement_types = df["measurement_type"].unique().to_list()
    measurement_data = {}
    for measurement_type in measurement_types:
        measurements = df.filter(df["measurement_type"] == measurement_type)
        company_measurement_ids = measurements["company_measurement_id"].to_list()
        measurement_table = f"measurement_{measurement_type}_value"
        measurement_data[measurement_type] = fetch_measurement_data(
            company_measurement_ids, measurement_table
        )
    return df, measurement_data
