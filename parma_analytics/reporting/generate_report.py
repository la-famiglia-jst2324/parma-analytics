import pandas as pd
from generate_html import generate_html_report
from parma_analytics.bl.generate_report import generate_report

df, measurement_data = generate_report()
html = generate_html_report(
    df,
    measurement_data.get("int", pd.DataFrame()),
    measurement_data.get("float", pd.DataFrame()),
    measurement_data.get("comment", pd.DataFrame()),
)
