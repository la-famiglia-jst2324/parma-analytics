from fastapi import APIRouter

from parma_analytics.api.models.crawling_finished import (
    ApiCrawlingFinishedCreateIn,
    ApiCrawlingFinishedCreateOut,
)


router = APIRouter()


@router.post(
    "/crawling-finished",
    status_code=201,
    description="Endpoint to receive notifications when all crawling jobs have completed. This allows the system to proceed with data processing once all data has been gathered.",
)
def crawling_finished(done_message: ApiCrawlingFinishedCreateIn):
    ## Later specify the trigger flow here
    print(done_message.incoming_message)
    # Return a JSON response
    return ApiCrawlingFinishedCreateOut(
        incoming_message=done_message.incoming_message,
        return_message="Notified about crawling finished",
    )
