import pytest
from datetime import datetime
from parma_analytics.sourcing.normalization.normalization_engine import (
    build_lookup_dict,
    process_data_point,
    normalize_data,
)
from parma_analytics.sourcing.normalization.normalization_model import NormalizedData


def test_build_lookup_dict():
    mapping_schema = {
        "Mappings": [
            {
                "source_field": "name",
                "type": "text",
                "source_measurement_id": "GH001",
            },
        ]
    }
    lookup_dict = build_lookup_dict(mapping_schema)
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
    assert result.timeStamp == datetime.fromisoformat("2023-01-01T00:00:00Z")
    assert result.value == "Langfuse"


def test_normalize_data():
    raw_data = {
        "company_id": "123",
        "timestamp": "2023-01-01T00:00:00Z",
        "data": [
            {
                "name": "Langfuse",
                "description": "Open-source analytics for LLM applications",
                "url": "https://github.com/langfuse",
                "repos": [
                    {
                        "repo_name": "langfuse",
                        "repo_description": "Open source observability and analytics for LLM applications",
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
            },
        ],
    }
    mapping_schema = {
        "Source": "GitHub",
        "Mappings": [
            {
                "source_field": "name",
                "type": "text",
                "measurement_name": "company name",
                "source_measurement_id": "GH001",
            },
            {
                "source_field": "description",
                "type": "paragraph",
                "measurement_name": "company description",
                "source_measurement_id": "GH002",
            },
            {
                "source_field": "url",
                "type": "link",
                "measurement_name": "github url",
                "source_measurement_id": "GH003",
            },
            {
                "source_field": "repos",
                "type": "nested",
                "measurement_name": "repositories",
                "source_measurement_id": "GH004",
                "NestedMappings": [
                    {
                        "source_field": "repo_name",
                        "type": "text",
                        "measurement_name": "repository name",
                        "source_measurement_id": "GH005",
                    },
                    {
                        "source_field": "repo_description",
                        "type": "paragraph",
                        "measurement_name": "repository description",
                        "source_measurement_id": "GH006",
                    },
                    {
                        "source_field": "language",
                        "type": "text",
                        "measurement_name": "repository primary language",
                        "source_measurement_id": "GH007",
                    },
                    {
                        "source_field": "created_at",
                        "type": "date",
                        "measurement_name": "repository creation date",
                        "source_measurement_id": "GH008",
                    },
                    {
                        "source_field": "updated_at",
                        "type": "date",
                        "measurement_name": "repository last updated date",
                        "source_measurement_id": "GH009",
                    },
                    {
                        "source_field": "pushed_at",
                        "type": "date",
                        "measurement_name": "repository last pushed date",
                        "source_measurement_id": "GH010",
                    },
                    {
                        "source_field": "html_url",
                        "type": "link",
                        "measurement_name": "repository html url",
                        "source_measurement_id": "GH011",
                    },
                    {
                        "source_field": "clone_url",
                        "type": "link",
                        "measurement_name": "repository clone url",
                        "source_measurement_id": "GH012",
                    },
                    {
                        "source_field": "svn_url",
                        "type": "link",
                        "measurement_name": "repository svn url",
                        "source_measurement_id": "GH013",
                    },
                    {
                        "source_field": "homepage",
                        "type": "link",
                        "measurement_name": "repository homepage url",
                        "source_measurement_id": "GH014",
                    },
                    {
                        "source_field": "size",
                        "type": "int",
                        "measurement_name": "repository size",
                        "source_measurement_id": "GH015",
                    },
                    {
                        "source_field": "stargazers_count",
                        "type": "int",
                        "measurement_name": "repository stargazers count",
                        "source_measurement_id": "GH016",
                    },
                    {
                        "source_field": "watchers_count",
                        "type": "int",
                        "measurement_name": "repository watchers count",
                        "source_measurement_id": "GH017",
                    },
                    {
                        "source_field": "forks_count",
                        "type": "int",
                        "measurement_name": "repository forks count",
                        "source_measurement_id": "GH018",
                    },
                    {
                        "source_field": "open_issues_count",
                        "type": "int",
                        "measurement_name": "repository open issues count",
                        "source_measurement_id": "GH019",
                    },
                    {
                        "source_field": "stars",
                        "type": "int",
                        "measurement_name": "repository stars",
                        "source_measurement_id": "GH020",
                    },
                    {
                        "source_field": "forks",
                        "type": "int",
                        "measurement_name": "repository forks",
                        "source_measurement_id": "GH021",
                    },
                ],
            },
        ],
    }

    normalized_data = normalize_data(raw_data, mapping_schema)
    assert isinstance(normalized_data, list)
