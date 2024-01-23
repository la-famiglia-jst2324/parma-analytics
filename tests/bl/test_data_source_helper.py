from unittest import mock
from unittest.mock import patch

import httpx
import pytest

from parma_analytics.bl.data_source_helper import ensure_appropriate_scheme


@pytest.fixture
def mock_os_getenv():
    with patch("os.getenv") as mock_getenv:
        mock_getenv.return_value = "prod"
        yield mock_getenv


@pytest.mark.parametrize(
    "deployment_env, url, expected_scheme",
    [
        ("local", "http://example.com", "http"),
        ("local", "https://example.com", "http"),
        ("local", "example.com", "http"),
        ("prod", "http://example.com", "https"),
        ("prod", "https://example.com", "https"),
        ("prod", "example.com", "https"),
        ("staging", "http://example.com", "https"),
        ("staging", "https://example.com", "https"),
        ("staging", "example.com", "https"),
    ],
)
def test_ensure_appropriate_scheme_success(
    deployment_env, url, expected_scheme, mock_os_getenv
):
    # Setup
    mock_os_getenv.return_value = deployment_env

    # Run the Test
    result = ensure_appropriate_scheme(url)

    # Assertions
    if result:
        assert result.startswith(
            expected_scheme
        ), f"URL scheme should be {expected_scheme} for deployment_env={deployment_env}"


@pytest.mark.parametrize(
    "deployment_env, url, expected_scheme",
    [
        ("local", "htt.://example.com", "http"),
        ("prod", "htt.://example.com", "https"),
        ("staging", "htt.://example.com", "https"),
    ],
)
def test_ensure_appropriate_scheme_error(
    deployment_env, url, expected_scheme, mock_os_getenv
):
    # Setup
    mock_os_getenv.return_value = deployment_env

    # Run the Test
    with mock.patch("httpx.URL", side_effect=httpx.InvalidURL(f"Invalid URL: {url}")):
        result = ensure_appropriate_scheme(url)

    # Assertions
    assert result is None, "URL scheme should be None due to InvalidURL"


def test_ensure_appropriate_scheme_error_empty_parameter():
    result = ensure_appropriate_scheme("")

    # Assertions
    assert result is None, "Result should be None due to None parameter"
