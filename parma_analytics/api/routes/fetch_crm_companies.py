"""API route for crm-companies."""
from fastapi import APIRouter, status
from pydantic import BaseModel

from parma_analytics.bl.fetch_crm_companies import get_new_crm_companies_bll

router = APIRouter()


class UserId(BaseModel):
    """Request body model."""

    user_id: int


@router.post(
    "/crm-companies",
    status_code=status.HTTP_200_OK,
    description=(
        "Triggers fetching companies from the CRM and registering "
        "them . Returns newly added companies if available."
    ),
)
def trigger_fetch_new_companies(user_id: UserId) -> str:
    """Returns the new companies retrieved from the CRM after storing them to the DB."""
    new_companies = get_new_crm_companies_bll(user_id)

    return new_companies
