
import json
from http import HTTPStatus
from fastapi import APIRouter, HTTPException, status
from parma_analytics.api.models.notifications import NotificationOut

# TODO: add authentication to the endpoint

router = APIRouter()

@router.post("/notifications", status_code=status.HTTP_201_CREATED,
            description="Endpoint to create a notification based on rules")
def check_rules_create_notification(notification: NotificationOut):
    """Checks the rules and creates a notification if the rules are met."""
    # queries to execute to get the rules based on the source_measurement_id
    
    
    