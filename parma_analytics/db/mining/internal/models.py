"""Generic firebase abstraction layer."""
from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

FirestoreFieldTypes = Literal[
    "string",
    "number",
    "boolean",
    "timestamp",
    "array",
    "map",
    "null",
    "geopoint",
    "reference",
]
# parma.mining.datasource.reddit
# parma_collection.


class Collection(BaseModel):
    """Collections are like singletons.

    They are containers for documents.
    """ ""

    name: str = Field(..., pattern=r"^[a-z0-9_-]+$")
    docs: DocTemplate | dict[str, Doc] = Field(default_factory=dict)


class DocField(BaseModel):
    """Fields are the building blocks of documents containing data."""

    name: str = Field(..., pattern=r"^[a-zA-Z0-9_-]+$")
    type: FirestoreFieldTypes
    required: bool = Field(True)


class _BaseTemplate(BaseModel):
    collections: dict[str, Collection] = Field(default_factory=dict)
    """Template for subcollections enforced in template instances."""

    fields: dict[str, DocField] = Field(default_factory=dict)


class DocTemplate(_BaseTemplate):
    """Documents are structures holding data.

    This model is the generic build plan for documents of the same type.
    """

    instances: dict[str, DocTemplateInstance] = Field(default_factory=dict)
    """Maps document names to concrete document instances following the template."""


class _BaseDoc(BaseModel):
    name: str = Field(..., pattern=r"^[a-z0-9_-]+$")
    values: dict[str, Any] = Field(default_factory=dict)
    """Maps field names to values."""


class DocTemplateInstance(_BaseDoc):
    """Documents are structures holding data.

    In contrast to DocTemplate this model describes a certain instance of a template.
    """

    pass


class Doc(_BaseTemplate, _BaseDoc):
    """Documents are structures holding data.

    Document that is defined in code and does not follow a template.
    """

    pass
