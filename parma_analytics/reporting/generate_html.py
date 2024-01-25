"""Generates an HTML report from a template and data."""

from jinja2 import Template


def generate_html_report(news_by_company) -> str:
    """Generate an HTML report from a template and data.

    Args:
        news_by_company: News info related to a company

    Returns:
        An HTML report.
    """
    with open(
        "parma_analytics/reporting/report_template/template.html"
    ) as template_file:
        template_string = template_file.read()

    template = Template(template_string)

    html_content = template.render(news_by_company=news_by_company)
    return html_content
