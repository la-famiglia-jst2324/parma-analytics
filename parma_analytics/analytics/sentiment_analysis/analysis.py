"""Test for sentiment analysis."""

from parma_analytics.analytics.sentiment_analysis.gpt_api import get_sentiment
from parma_analytics.db.prod.engine import get_session
from parma_analytics.db.prod.measurement_value_query import MeasurementValueCRUD
from parma_analytics.db.prod.models.measurement_value_models import (
    MeasurementCommentValue,
)

# TODO: 一开始是获取所有的comment，评分并储存。后面应该是有了新的comment就做分析。

comment_value_crud = MeasurementValueCRUD(MeasurementCommentValue)

# 使用 with 语句来获取 Session 实例
with get_session() as db_session:
    all_comment_values = comment_value_crud.list_measurement_value(db_session)

    # print(all_comment_values)
    for comment_value in all_comment_values:
        print(f"ID: {comment_value.id}, Comment: {comment_value.sentiment_score}")
        score = get_sentiment(comment_value.value)
        comment_value.sentiment_score = score
        print("\n")
        print(f"ID: {comment_value.id}, Comment: {comment_value.sentiment_score}")

    # commit to DB
    db_session.commit()
