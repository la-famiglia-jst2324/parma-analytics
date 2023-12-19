"""FastAPI routes for registering a new company from within a sourcing module."""

from fastapi import APIRouter
from starlette import status

from parma_analytics.api.models.new_company import (
    ApiNewCompanyCreateIn,
    ApiNewCompanyCreateOut,
)

router = APIRouter()


@router.post(
    "/new-company",
    status_code=status.HTTP_201_CREATED,
    description=(
        "Endpoint to receive a new company. The data is forwarded to the sourcing "
        "backend for registering and further processing."
    ),
)
def register_new_company(company: ApiNewCompanyCreateIn) -> ApiNewCompanyCreateOut:
    """Register a new company.

    Args:
        company: The new company to register.

    Returns:
        Acknowledgement message containing the company id and the company name.
    """
    # TODO: Validate or process the company data as needed.
    # TODO: Forward the company data to the Data Retrieval Controller backend.

    return ApiNewCompanyCreateOut(
        id=company.id,
        company_name=company.company_name,
        return_message="New company forwarded to data sourcing successfully",
    )
