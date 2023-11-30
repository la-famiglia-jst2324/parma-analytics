from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from parma_analytics.db.prod.engine import get_db
from starlette import status

from parma_analytics.api.models.source_measurement import (
    ApiSourceMeasurementCreateIn,
    ApiSourceMeasurementCreateOut,
    ApiSourceMeasurementOut,
    ApiSourceMeasurementUpdateIn,
    ApiSourceMeasurementUpdateOut,
    ApiSourceMeasurementDeleteOut,
)

from parma_analytics.bl.source_measurement_bll import (
    create_source_measurement_bll,
    read_source_measurement_bll,
    update_source_measurement_bll,
    delete_source_measurement_bll,
    list_source_measurements_bll,
)

router = APIRouter()


@router.post(
    "/source-measurement",
    status_code=status.HTTP_201_CREATED,
    description="Create a new source measurement.",
)
async def create_source_measurement(
    source_measurement: ApiSourceMeasurementCreateIn, db: Session = Depends(get_db)
) -> ApiSourceMeasurementCreateOut:
    print(source_measurement)
    created_source_measurement_id = create_source_measurement_bll(
        db, source_measurement
    )
    return ApiSourceMeasurementCreateOut(
        id=created_source_measurement_id,
        creation_msg="Source Measurement successfully created",
    )


@router.get(
    "/source-measurement",
    status_code=status.HTTP_200_OK,
    description="List all source measurements with pagination.",
)
def read_all_source_measurements(
    db: Session = Depends(get_db),
    page: int = 1,
    per_page: int = 10,
) -> List[ApiSourceMeasurementOut]:
    source_measurements = list_source_measurements_bll(db, page, per_page)
    return [ApiSourceMeasurementOut(**dict(sm)) for sm in source_measurements]


@router.get(
    "/source-measurement/{source_measurement_id}",
    status_code=status.HTTP_200_OK,
    description="Get details of a specific source measurement.",
)
async def read_source_measurement(
    source_measurement_id: int, db: Session = Depends(get_db)
) -> ApiSourceMeasurementOut:
    retrieved_source_measurement = read_source_measurement_bll(
        db, source_measurement_id
    )
    return ApiSourceMeasurementOut(**dict(retrieved_source_measurement))


@router.put(
    "/source-measurement/{source_measurement_id}",
    status_code=status.HTTP_202_ACCEPTED,
    description="Update details of a specific source measurement.",
)
async def update_source_measurement(
    source_measurement_id: int,
    source_measurement: ApiSourceMeasurementUpdateIn,
    db: Session = Depends(get_db),
) -> ApiSourceMeasurementUpdateOut:
    updated_source_measurement = update_source_measurement_bll(
        db, source_measurement_id, source_measurement
    )
    return ApiSourceMeasurementUpdateOut(**dict(updated_source_measurement))


@router.delete(
    "/source-measurement/{source_measurement_id}",
    status_code=status.HTTP_200_OK,
    description="Delete a specific source measurement.",
)
async def delete_source_measurement(
    source_measurement_id: int, db: Session = Depends(get_db)
) -> ApiSourceMeasurementDeleteOut:
    delete_source_measurement_bll(db, source_measurement_id)
    return ApiSourceMeasurementDeleteOut(
        deletion_msg=f"Source measurement {source_measurement_id} has been deleted."
    )
