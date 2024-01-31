"""FastAPI routes notification rules."""

import logging

from fastapi import APIRouter, Response, status

from parma_analytics.db.populate_notification_rule import populate_notification_rules

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get(
    "/notification-rules",
    status_code=status.HTTP_200_OK,
    description="Endpoint to populate notification rules.",
)
async def notification_rules() -> Response:
    """Poulates the notification rules entity."""
    try:
        populate_notification_rules()

        return Response(content="Rules table updated", status_code=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error creating rules table: {str(e)}")

        return Response(
            content="Internal Server Error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
