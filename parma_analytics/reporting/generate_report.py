from generate_html import generate_html_report
from generate_pdf import generate_pdf

from parma_analytics.bl.generate_report import generate_report

df, measurement_data = generate_report()
html_content = generate_html_report(df, measurement_data)
generate_pdf(html_content, "Analysis Report for Companies.pdf")
