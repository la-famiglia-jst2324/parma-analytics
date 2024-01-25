"""FastAPI routes generating and sending reports."""

import logging

from fastapi import APIRouter, Response, status

from parma_analytics.reporting.send_reports import send_reports

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get(
    "/weekly-reports",
    status_code=status.HTTP_200_OK,
    description="Endpoint to generate weekly reports and send it to user.",
)
async def weeky_reports() -> Response:
    """Retrieve the reports from news entity and send it via email and slack."""
    try:
        send_reports()

        return Response(
            content="Weekly reports sent successfully", status_code=status.HTTP_200_OK
        )
    except Exception as e:
        logger.error(f"Error generating and sending weekly reports: {str(e)}")

        return Response(
            content="Internal Server Error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
