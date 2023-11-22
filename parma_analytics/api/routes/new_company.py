from fastapi import APIRouter, HTTPException
import requests


from parma_analytics.api.models.new_company import (
    ApiNewCompanyCreateIn,
    ApiNewCompanyCreateOut,
)

router = APIRouter()


@router.post(
    "/new-company",
    status_code=201,
    description="Endpoint to receive a new company. The data is forwarded to the sourcing backend for registering and further processing.",
)
def register_new_company(company: ApiNewCompanyCreateIn):
    # Validate or process the company data as needed.

    # Forward the company data to another backend
    try:
        # TODO: change the sourcing url once provided.
        response = requests.post("http://sourcing-backend/api/receive-company", company)
        response.raise_for_status()
    except requests.HTTPError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error forwarding company to the data sourcing modules: {str(e)}",
        )

    return ApiNewCompanyCreateOut(
        company_name=company.company_name,
        return_message="New company forwarded to data sourcing successfully",
    )
