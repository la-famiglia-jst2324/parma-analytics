"""Helper to adapt the URL schema."""
import logging
import os

import httpx


def ensure_appropriate_scheme(url: str) -> str | None:
    """Adapt the URL scheme based on the deployment environment."""
    if not url:
        return None

    try:
        env = os.getenv("DEPLOYMENT_ENV", "local").lower()

        if "://" not in url:
            default_scheme = "https" if env in ["prod", "staging"] else "http"
            url = f"{default_scheme}://{url}"

        parsed_url = httpx.URL(url)

        scheme_lower = parsed_url.scheme.lower()
        if env in ["prod", "staging"] and scheme_lower != "https":
            return parsed_url.copy_with(scheme="https").__str__()
        elif env not in ["prod", "staging"] and scheme_lower != "http":
            return parsed_url.copy_with(scheme="http").__str__()

        return url
    except httpx.InvalidURL:
        logging.error(f"Invalid URL: {url}")
        return None
