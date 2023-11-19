from fastapi import APIRouter, HTTPException, Body
from fastapi.encoders import jsonable_encoder
import httpx
from pydantic import BaseModel

router = APIRouter()


# To be extended when needed.
class Company(BaseModel):
    id: int
    name: str
    description: str
    added_by: str


@router.post("/new-company", status_code=201)
async def register_new_company(company: Company = Body(..., embed=True)):
    # Validate or process the company data as needed

    # Forward the company data to another backend
    try:
        async with httpx.AsyncClient() as client:
            # TODO: change the sourcing url once provided.
            response = await client.post(
                "http://sourcing-backend/api/receive-company", json=company.model_dump()
            )
            response.raise_for_status()
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error forwarding company to the data sourcing modules: {str(e)}",
        )

    return jsonable_encoder(
        {"message": "New company forwarded to data sourcing successfully"}
    )
