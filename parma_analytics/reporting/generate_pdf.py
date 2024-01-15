import io

from weasyprint import HTML


def generate_pdf(html_content, css_styles=None):
    """Generate PDF."""
    pdf_options = {
        "page-size": "A4",
        "margin-top": "5mm",
        "margin-right": "1mm",
        "margin-bottom": "10mm",
        "margin-left": "1mm",
    }

    pdf_buffer = io.BytesIO()
    html = HTML(string=html_content, base_url=".")
    html.write_pdf(pdf_buffer, **pdf_options)

    pdf_buffer.seek(0)
    return pdf_buffer.read()
