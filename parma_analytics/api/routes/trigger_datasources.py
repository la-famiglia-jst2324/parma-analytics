from fastapi import APIRouter
from starlette import status

from parma_analytics.api.models.trigger_datasources import (
    ApiTriggerDataSourcesCreateIn,
    ApiTriggerDataSourcesCreateOut,
)

router = APIRouter()


@router.post(
    "/trigger-datasources/",
    status_code=status.HTTP_201_CREATED,
    description="""Endpoint to receive the trigger for the data sources.
        Expects a dictionary of data source ids as keys and the company ids for which they will be triggered as values.""",
)
async def create_trigger_data_sources(body: ApiTriggerDataSourcesCreateIn):
    # the dictionary containing the module ids and company ids.
    trigger_data = body.trigger_data

    # Later specify the trigger flow here
    print(trigger_data)

    # Return the output model
    return ApiTriggerDataSourcesCreateOut(
        return_message="Trigger data sources created successfully",
    )
