from datetime import datetime

import pytest

from parma_analytics.db.mining.models import NormalizationSchema, RawData
from parma_analytics.sourcing.normalization.normalization_engine import (
    build_lookup_dict,
    normalize_data,
    process_data_point,
)
from parma_analytics.sourcing.normalization.normalization_model import NormalizedData


@pytest.fixture
def mapping_schema() -> NormalizationSchema:
    data_dict = {
        "Source": "GitHub",
        "Mappings": [
            {
                "SourceField": "name",
                "DataType": "text",
                "MeasurementName": "company name",
                "source_measurement_id": "GH001",
            },
            {
                "SourceField": "description",
                "DataType": "paragraph",
                "MeasurementName": "company description",
                "source_measurement_id": "GH002",
            },
            {
                "SourceField": "url",
                "DataType": "link",
                "MeasurementName": "github url",
                "source_measurement_id": "GH003",
            },
            {
                "SourceField": "repos",
                "DataType": "nested",
                "MeasurementName": "repositories",
                "source_measurement_id": "GH004",
                "NestedMappings": [
                    {
                        "SourceField": "repo_name",
                        "DataType": "text",
                        "MeasurementName": "repository name",
                        "source_measurement_id": "GH005",
                    },
                    {
                        "SourceField": "repo_description",
                        "DataType": "paragraph",
                        "MeasurementName": "repository description",
                        "source_measurement_id": "GH006",
                    },
                    {
                        "SourceField": "language",
                        "DataType": "text",
                        "MeasurementName": "repository primary language",
                        "source_measurement_id": "GH007",
                    },
                    {
                        "SourceField": "created_at",
                        "DataType": "date",
                        "MeasurementName": "repository creation date",
                        "source_measurement_id": "GH008",
                    },
                    {
                        "SourceField": "updated_at",
                        "DataType": "date",
                        "MeasurementName": "repository last updated date",
                        "source_measurement_id": "GH009",
                    },
                    {
                        "SourceField": "pushed_at",
                        "DataType": "date",
                        "MeasurementName": "repository last pushed date",
                        "source_measurement_id": "GH010",
                    },
                    {
                        "SourceField": "html_url",
                        "DataType": "link",
                        "MeasurementName": "repository html url",
                        "source_measurement_id": "GH011",
                    },
                    {
                        "SourceField": "clone_url",
                        "DataType": "link",
                        "MeasurementName": "repository clone url",
                        "source_measurement_id": "GH012",
                    },
                    {
                        "SourceField": "svn_url",
                        "DataType": "link",
                        "MeasurementName": "repository svn url",
                        "source_measurement_id": "GH013",
                    },
                    {
                        "SourceField": "homepage",
                        "DataType": "link",
                        "MeasurementName": "repository homepage url",
                        "source_measurement_id": "GH014",
                    },
                    {
                        "SourceField": "size",
                        "DataType": "int",
                        "MeasurementName": "repository size",
                        "source_measurement_id": "GH015",
                    },
                    {
                        "SourceField": "stargazers_count",
                        "DataType": "int",
                        "MeasurementName": "repository stargazers count",
                        "source_measurement_id": "GH016",
                    },
                    {
                        "SourceField": "watchers_count",
                        "DataType": "int",
                        "MeasurementName": "repository watchers count",
                        "source_measurement_id": "GH017",
                    },
                    {
                        "SourceField": "forks_count",
                        "DataType": "int",
                        "MeasurementName": "repository forks count",
                        "source_measurement_id": "GH018",
                    },
                    {
                        "SourceField": "open_issues_count",
                        "DataType": "int",
                        "MeasurementName": "repository open issues count",
                        "source_measurement_id": "GH019",
                    },
                    {
                        "SourceField": "stars",
                        "DataType": "int",
                        "MeasurementName": "repository stars",
                        "source_measurement_id": "GH020",
                    },
                    {
                        "SourceField": "forks",
                        "DataType": "int",
                        "MeasurementName": "repository forks",
                        "source_measurement_id": "GH021",
                    },
                ],
            },
        ],
    }

    return NormalizationSchema(
        id="123",
        create_time=datetime.now(),
        update_time=None,
        read_time=None,
        schema=data_dict,
    )


@pytest.fixture
def raw_data() -> RawData:
    raw_data = {
        "name": "Langfuse",
        "description": "Open-source analytics for LLM applications",
        "url": "https://github.com/langfuse",
        "repos": [
            {
                "repo_name": "langfuse",
                "repo_description": "Open source observability and analytics for LLM applications",  # noqa
                "stars": 1531,
                "forks": 121,
                "language": "TypeScript",
                "created_at": "2023-05-18T17:47:09Z",
                "updated_at": "2023-12-07T05:04:52Z",
                "pushed_at": "2023-12-06T22:59:57Z",
                "html_url": "https://github.com/langfuse/langfuse",
                "clone_url": "https://github.com/langfuse/langfuse.git",
                "svn_url": "https://github.com/langfuse/langfuse",
                "homepage": "https://langfuse.com",
                "size": 4849,
                "stargazers_count": 1531,
                "watchers_count": 1531,
                "forks_count": 121,
                "open_issues_count": 49,
            }
        ],
    }

    return RawData(
        id="123",  # Example ID
        create_time=datetime.now(),
        update_time=None,
        read_time=None,
        company_id="1234",
        mining_trigger="example_trigger",
        status="success",
        data=raw_data,
    )


def test_build_lookup_dict(mapping_schema: NormalizationSchema):
    lookup_dict = build_lookup_dict(mapping_schema.schema)

    assert "name" in lookup_dict
    assert lookup_dict["name"]["type"] == "text"


def test_process_data_point():
    mapping = {
        "source_measurement_id": "GH001",
        "type": "text",
    }
    result = process_data_point("Langfuse", "123", "2023-01-01T00:00:00Z", mapping)
    assert isinstance(result, NormalizedData)
    assert result.company_id == "123"
    assert result.timestamp == datetime.fromisoformat("2023-01-01T00:00:00Z")
    assert result.value == "Langfuse"


def test_normalize_data(raw_data: RawData, mapping_schema: NormalizationSchema):
    normalized_data = normalize_data(raw_data, mapping_schema)
    assert isinstance(normalized_data, list)
    assert all(isinstance(item, NormalizedData) for item in normalized_data)
