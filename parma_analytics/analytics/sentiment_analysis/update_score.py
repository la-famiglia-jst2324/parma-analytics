"""Function for updating sentiment analysis score in DB."""

import logging

from parma_analytics.analytics.sentiment_analysis.sentiment_analysis import (
    get_sentiment,
)
from parma_analytics.db.prod.engine import get_session
from parma_analytics.db.prod.measurement_value_query import MeasurementValueCRUD
from parma_analytics.db.prod.models.measurement_value_models import (
    MeasurementCommentValue,
)

logger = logging.getLogger(__name__)


async def update_scores(ids: list) -> list | None:
    """Update sentiment scores of all given comment values in DB.

    Args:
        ids: The comment value ids.

    Returns:
        A list of scores representing the score of the given comments.
    """
    comment_value_crud = MeasurementValueCRUD(MeasurementCommentValue)
    values = []  # all comments

    with get_session() as db_session:
        for id in ids:
            comment_value = comment_value_crud.get_measurement_value(db_session, id)
            values.append(comment_value.value)
        sentiment_score_list = await get_sentiment(values)
        # Ensure that score[i] is an integer before assigning
        scores = []

        for item in sentiment_score_list:
            try:
                int_item = int(item)
                scores.append(int_item)
            except ValueError:
                continue
        logger.debug(scores)

        try:
            for i, id in enumerate(ids):
                comment_value = comment_value_crud.get_measurement_value(db_session, id)
                comment_value.sentiment_score = scores[i]
            # Commit all the changes after the loop
            db_session.commit()

        except Exception as e:
            # Rollback in case of error
            db_session.rollback()
            raise e  # Reraise the exception to handle it or log it as needed

    return sentiment_score_list
