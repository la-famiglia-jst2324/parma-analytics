import pandas as pd
import sys

sys.path.append("/mnt/d/Deepankar/TUM/Study Material/Praktikum/AllCode/parma-analytics")
from generate_html import generate_html_report
from parma_analytics.bl.generate_report import generate_report
from generate_pdf import generate_pdf

df, measurement_data = generate_report()
html_content = generate_html_report(
    df,
    measurement_data.get("int", pd.DataFrame()),
    measurement_data.get("float", pd.DataFrame()),
    measurement_data.get("comment", pd.DataFrame()),
    measurement_data.get("text", pd.DataFrame()),
    measurement_data.get("paragraph", pd.DataFrame()),
)
generate_pdf(html_content, "Analysis Report for Companies.pdf")
