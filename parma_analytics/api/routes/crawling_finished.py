from fastapi import APIRouter

from parma_analytics.api.models.crawling_finished import (
    ApiCrawlingFinishedCreateIn,
    ApiCrawlingFinishedCreateOut,
)


router = APIRouter()


@router.post("/crawling-finished", status_code=201)
def crawling_finished(done_message: ApiCrawlingFinishedCreateIn):
    ## Later specify the trigger flow here
    print(done_message.incoming_message)
    # Return a JSON response
    return ApiCrawlingFinishedCreateOut(
        incoming_message=done_message.incoming_message,
        return_message="Notified about crawling finished",
    )
