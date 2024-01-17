"""Paginating utility for SQLAlchemy queries with decorator and query transformation."""

from collections.abc import Callable
from typing import TypeVar

from sqlalchemy.engine import Engine

ResponseModel = TypeVar("ResponseModel")
TCallable = TypeVar("TCallable", bound=Callable)


# ------------------------------------------------------------------------------------ #
#                                         Query                                        #
# ------------------------------------------------------------------------------------ #

Model = TypeVar("Model")


def update_model(engine: Engine, model: Model, fields: list[str]) -> Model:
    """Helper function to update a model only considering the given fields.

    Args:
        engine: The database engine.
        model: The model to update with the updated fields.
        fields: The fields to update.

    Returns:
        The updated model.
    """
    raise NotImplementedError
