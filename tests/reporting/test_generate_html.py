"""Test for generating HTML."""
from parma_analytics.reporting.generate_html import generate_html_report


def test_generate_html_report():
    """Test for generating html_report for email."""
    news_by_company = {
        "company1": ["News 1", "News 2"],
        "company2": ["News 3", "News 4"],
    }
    result = generate_html_report(news_by_company)

    assert isinstance(result, str)
    assert "company1" in result
    assert "News 1" in result
    assert "company2" in result
    assert "News 3" in result
