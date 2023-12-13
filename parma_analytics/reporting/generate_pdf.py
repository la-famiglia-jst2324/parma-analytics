from io import BytesIO
from xhtml2pdf import pisa


def fetch_resources(uri, rel):
    if uri.startswith("http") or uri.startswith("data:"):
        return uri
    return None


def generate_pdf(html_content, output_pdf):
    pdf_buffer = BytesIO()
    pisa.CreatePDF(
        BytesIO(html_content.encode("utf-8")),
        pdf_buffer,
        link_callback=fetch_resources,
    )

    pdf_buffer.seek(0)

    with open(output_pdf, "wb") as f:
        f.write(pdf_buffer.read())
