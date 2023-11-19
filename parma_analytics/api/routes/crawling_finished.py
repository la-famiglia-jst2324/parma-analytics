
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder


router = APIRouter()


@router.post("/crawling-finished", status_code=201)
def crawling_finished():
    
    ## Later specify the trigger flow here

    # Return a JSON response
    return jsonable_encoder({'message': 'Notified about crawling finished'})

