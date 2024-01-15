"""Generate pdf files."""

from io import BytesIO

from xhtml2pdf import pisa


def fetch_resources(uri: str):
    """Callback function that validates uri.

    Args:
        uri: The uri to validate.

    Returns:
        The uri if it is valid, None otherwise.
    """
    if uri.startswith("http") or uri.startswith("data:"):
        return uri
    return None


def generate_pdf(html_content: str) -> None:
    """Generates a PDF from the given HTML content.

    Args:
        html_content: The html source code to convert to PDF.

    Returns:
        The generated PDF as bytes.
    """
    pdf_buffer = BytesIO()
    output_pdf = pisa.CreatePDF(
        BytesIO(html_content.encode("utf-8")),
        pdf_buffer,
        link_callback=fetch_resources,
    )

    pdf_buffer.seek(0)

    with open(output_pdf, "wb") as f:
        f.write(pdf_buffer.read())
