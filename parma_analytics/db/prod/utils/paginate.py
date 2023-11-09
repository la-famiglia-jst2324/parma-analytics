"""Paginating utility for SQLAlchemy queries with decorator and query transformation."""

from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import Any, Generic, TypeVar, cast, overload

from sqlalchemy.orm.query import Query

# ------------------------------------------------------------------------------------ #
#                                        Modelx                                        #
# ------------------------------------------------------------------------------------ #

ElementType = TypeVar("ElementType")


@dataclass
class ListPaginationResult(Generic[ElementType]):
    """A paginated list of elements."""

    total_pages: int
    list: list[ElementType]


# ------------------------------------------------------------------------------------ #
#                                       Decorator                                      #
# ------------------------------------------------------------------------------------ #

ResponseModel = TypeVar("ResponseModel")
TCallable = TypeVar("TCallable", bound=Callable)


@overload
def paginate(
    func: None = None, *, default_page_size: int = 20
) -> Callable[[TCallable], TCallable]:
    ...


@overload
def paginate(
    func: TCallable,
    *,
    default_page_size: int = 20,
) -> TCallable:
    ...


def paginate(
    func: TCallable | None = None,
    *,
    default_page_size: int = 10,
) -> Callable[[TCallable], TCallable] | TCallable:
    """Paginate a SQLAlchemy query.

    Args:
        func: The function to decorate.
        default_page_size: The default number of items per page.

    Returns:
        The decorated function.

    Examples:
        ```
        @paginate
        def list_dummies(engine: Engine, *, page: int, page_size: int) -> list[DbDummy]:
            ...

        @paginate(page=1, page_size=20)
        def list_dummies(engine: Engine, *, page: int, page_size: int) -> list[DbDummy]:
        ```
    """
    if func is None:

        def outer_wrapper(func: TCallable) -> TCallable:
            """The outer wrapper function."""

            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> TCallable:
                """The wrapper function."""
                kwargs.update({"page": kwargs.get("page", 1)})
                kwargs.update({"page_size": kwargs.get("page_size", default_page_size)})
                return func(*args, **kwargs)

            return cast(TCallable, wrapper)

        return outer_wrapper

    else:

        @wraps(func)
        def wrapper(*args, **kwargs) -> TCallable:
            """The wrapper function."""
            kwargs.update(kwargs.get("page", 1))
            kwargs.update(kwargs.get("page_size", default_page_size or 20))
            return func(*args, **kwargs)

    return wrapper


# ------------------------------------------------------------------------------------ #
#                                         Query                                        #
# ------------------------------------------------------------------------------------ #

Model = TypeVar("Model")


def paginate_query(
    query: Query[Model], page: int = 1, page_size: int = 10
) -> ListPaginationResult[Model]:
    """Paginate a SQLAlchemy query.

    Args:
        session: The SQLAlchemy session to use.
        query: The SQLAlchemy query to paginate.
        page: The page number (1-based index).
        page_size: The number of items per page.

    Returns:
        A tuple containing the total number of pages and the queried objects for the requested page.
    """
    total_items = query.count()
    total_pages = (total_items + page_size - 1) // page_size
    page = max(1, min(page, total_pages))
    offset = (page - 1) * page_size

    paginated_query = query.offset(offset).limit(page_size)
    items = paginated_query.all()

    return ListPaginationResult(total_pages=total_pages, list=items)
