from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from parma_analytics.api.models.source_measurement import (
    ApiSourceMeasurementCreateIn,
    ApiSourceMeasurementCreateOut,
    ApiSourceMeasurementDeleteOut,
    ApiSourceMeasurementListOut,
    ApiSourceMeasurementOut,
    ApiSourceMeasurementUpdateIn,
    ApiSourceMeasurementUpdateOut,
)
from parma_analytics.bl.source_measurement_bll import (
    create_source_measurement_bll,
    delete_source_measurement_bll,
    list_source_measurements_bll,
    read_source_measurement_bll,
    update_source_measurement_bll,
)
from parma_analytics.db.prod.engine import get_session

router = APIRouter()


@router.post(
    "/source-measurement",
    status_code=status.HTTP_201_CREATED,
    description="Create a new source measurement.",
)
async def create_source_measurement(
    source_measurement: ApiSourceMeasurementCreateIn, db: Session = Depends(get_session)
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
    description=(
        "List all source measurements with pagination. Additionally returns "
        "the total number of pages."
    ),
)
def read_all_source_measurements(
    db: Session = Depends(get_session),
    page: int = 1,
    per_page: int = 10,
) -> ApiSourceMeasurementListOut:
    source_measurements = list_source_measurements_bll(db, page, per_page)
    measurements_out = [
        ApiSourceMeasurementOut(**dict(sm))
        for sm in source_measurements.measurements_list
    ]
    return ApiSourceMeasurementListOut(
        measurements_list=measurements_out, num_pages=source_measurements.num_pages
    )


@router.get(
    "/source-measurement/{source_measurement_id}",
    status_code=status.HTTP_200_OK,
    description="Get details of a specific source measurement.",
)
async def read_source_measurement(
    source_measurement_id: int, db: Session = Depends(get_session)
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
    db: Session = Depends(get_session),
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
    source_measurement_id: int, db: Session = Depends(get_session)
) -> ApiSourceMeasurementDeleteOut:
    delete_source_measurement_bll(db, source_measurement_id)
    return ApiSourceMeasurementDeleteOut(
        deletion_msg=f"Source measurement {source_measurement_id} has been deleted."
    )
