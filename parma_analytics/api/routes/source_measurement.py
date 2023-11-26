from fastapi import APIRouter, Depends
from pydantic import UUID4
from sqlalchemy.orm import Session
from parma_analytics.db.prod.engine import get_db

# Import your models from the models file
from parma_analytics.api.models.source_measurement import (
    ApiSourceMeasurementCreateIn,
    ApiSourceMeasurementCreateOut,
    ApiSourceMeasurementOut,
    ApiSourceMeasurementUpdateIn,
    ApiSourceMeasurementUpdateOut,
)

from parma_analytics.bl.source_measurement_bll import (
    create_source_measurement_bll,
    read_source_measurement_bll,
    update_source_measurement_bll,
    delete_source_measurement_bll,
    list_source_measurements_bll,
)
from parma_analytics.db.prod.utils.paginate import ListPaginationResult

router = APIRouter()


@router.post("/source-measurement", status_code=201)
def create_source_measurement(
    source_measurement: ApiSourceMeasurementCreateIn, db: Session = Depends(get_db)
) -> ApiSourceMeasurementCreateOut:
    """SourceMeasurement POST endpoint for the API.

    Args:
        source_measurement: The SourceMeasurement object to create.
    """
    created_source_measurement = create_source_measurement_bll(db, source_measurement)

    # hand over to business logic layer and transform the result to the API model again
    return ApiSourceMeasurementCreateOut(created_source_measurement)


'''
@router.get("/source-measurement", status_code=200)
def read_all_source_measurements(
    page: int = 5,
    per_page: int = 10,
) -> [ApiSourceMeasurementCreateOut]:
    """SourceMeasurement POST endpoint for the API.

    Args:
        page: The page number.
        per_page: The number of items per page.
    """
    source_measurement = list_source_measurements_bll(page, per_page)

    # hand over to business logic layer and transform the result to the API model again
    return [ApiSourceMeasurementCreateOut(source_measurement)]
'''


@router.get("/source-measurement/{source_measurement_id}", status_code=200)
def read_source_measurement(
    source_measurement_id: UUID4, db: Session = Depends(get_db)
) -> ApiSourceMeasurementOut:
    """SourceMeasurement GET endpoint for the API.

    Args:
        source_measurement_id: The ID of the SourceMeasurement.
    """

    # fetch from the database layer through the business logic layer
    retrieved_source_measurement = read_source_measurement_bll(
        db, source_measurement_id
    )

    return ApiSourceMeasurementOut(retrieved_source_measurement)


@router.put("/source_measurement/{source_measurement_id}", status_code=202)
def update_source_measurement(
    source_measurement_id: UUID4,
    source_measurement: ApiSourceMeasurementUpdateIn,
    db: Session = Depends(get_db),
) -> ApiSourceMeasurementUpdateOut:
    """SourceMeasurement PUT endpoint for the API.

    Args:
        source_measurement_id: The ID of the SourceMeasurement.
        source_measurement: The SourceMeasurement object to update.
    """
    # hand over to business logic layer and transform the result to the API model again
    updated_source_measurement = update_source_measurement_bll(
        db, source_measurement_id, source_measurement
    )

    return ApiSourceMeasurementUpdateOut(updated_source_measurement)


@router.delete("/source_measurement/{source_measurement_id}", status_code=204)
def delete_source_measurement(
    source_measurement_id: UUID4, db: Session = Depends(get_db)
) -> None:
    """SourceMeasurement DELETE endpoint for the API.

    Args:
        source_measurement_id: The ID of the SourceMeasurement.
    """
    # hand over to business logic layer
    delete_source_measurement_bll(db, source_measurement_id)
    pass
