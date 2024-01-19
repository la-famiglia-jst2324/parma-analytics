# function
#   - create news
# fetches rules based on the source_measurement_id given to the function
# compares the new notification based on the rules by getting and comparing with 
# the previous notification from the database that belongs to the same source_measurement_id

from parma_analytics.api.models.news import ApiNewsIn
from parma_analytics.db.prod.source_measurement_query import get_source_measurement_query


def check_rules_create_notification(news: ApiNewsIn):
    # News(source_measurement_id) -> CompanySourceMeasurement(sourceMeasurementId, companyMeasurementId) -> SourceMasurement(source_measurement_id = id): TYPE -> MeasurementTYPEValue(companyMeasurementId)
    source_measurement_id = news.source_measurement_id
    trigger_factor = news.trigger_factor
    timestamp = news.timestamp
    id = news.id
    
    # get the source_measurement type
    source_measurement = get_source_measurement_query(engine, source_measurement_id)
