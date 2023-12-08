from parma_analytics.analytics.visualization.fetch_data import fetch_int_data
from parma_analytics.analytics.visualization.create_chart import (
    create_time_series_chart,
)
from generate_pdf import export_to_pdf

db_params = {
    "database": "parma-prod-db",
    "user": "parma-prod-db",
    "password": "parma-prod-db",
    "host": "localhost",
    "port": 9000,
}
provided_measurement_id = 7

# Fetch data
df = fetch_int_data(db_params, provided_measurement_id)

# Convert Polars DataFrame to Pandas DataFrame
df_pandas = df.to_pandas()

# Create chart
plt = create_time_series_chart(df_pandas, "Time Series Data", "Date", "Value")

# Export to PDF
export_to_pdf(plt, "output.pdf")
