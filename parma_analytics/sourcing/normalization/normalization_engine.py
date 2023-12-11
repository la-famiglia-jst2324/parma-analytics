from datetime import datetime
from typing import Any

from parma_analytics.db.mining.models import RawData, NormalizationSchema
from parma_analytics.sourcing.normalization.normalization_model import NormalizedData


def build_lookup_dict(mapping_schema: dict[str, Any]) -> dict[str, dict[str, str]]:
    """Constructs a recursive lookup dictionary from a mapping schema.

    Args:
    mapping_schema (dict): The mapping schema containing the fields and their types.

    Returns:
    dict[str, dict[str, str]]: A dictionary for looking up the types and source measurement IDs by source field.
    """
    lookup_dict: dict[str, dict[str, str]] = {}

    def add_mappings(mappings: list, parent_dict: dict):
        try:
            for mapping in mappings:
                source_field = mapping.get("SourceField")
                if source_field:
                    parent_dict[source_field] = {
                        "type": mapping.get("DataType"),
                        "source_measurement_id": mapping.get("source_measurement_id"),
                    }

                    # Handle nested mappings recursively
                    if mapping.get("DataType") == "nested":
                        nested_mappings = mapping.get("NestedMappings", [])
                        add_mappings(nested_mappings, parent_dict)
        except KeyError as e:
            print(f"Error processing mapping schema: missing key {e}")

    add_mappings(mapping_schema.get("Mappings", []), lookup_dict)
    return lookup_dict


def process_data_point(
    value: str, company_id: str, timestamp: str, mapping: dict[str, str]
) -> NormalizedData:
    """Processes a single data point according to its mapping.

    Args:
    value (Any): The value of the data point.
    company_id (str): The ID of the company.
    timestamp (str): The timestamp of the data.
    mapping (dict[str, Any]): The mapping information for this data point.

    Returns:
    NormalizedData: A normalized data point.
    """
    return NormalizedData(
        source_measurement_id=mapping.get("source_measurement_id"),
        timeStamp=datetime.fromisoformat(timestamp),
        company_id=company_id,
        value=value,
        type=mapping.get("type"),
    )


def normalize_nested_data(
    nested_data: Any, company_id: str, timestamp: str, lookup_dict: dict[str, Any]
) -> list[NormalizedData]:
    """Recursively normalizes nested data according to the provided mapping schema.

    This function processes each nested item (which could itself be a nested structure) and normalizes it into
    instances of NormalizedData. It handles multiple levels of nested data by recursively calling itself when
    encountering further nested structures.

    Args:
    nested_data (Any): The nested data to be normalized. It can be a list of dicts (representing multiple nested items) or a single dict (representing one nested item).
    company_id (str): The ID of the company associated with the data.
    timestamp (str): The timestamp when the data was retrieved or processed.
    lookup_dict (Dict[str, Any]): A dictionary containing the mapping information for data normalization.

    Returns:
    List[NormalizedData]: A list of NormalizedData instances representing the normalized nested data.
    """
    normalized_results: list[NormalizedData] = []
    if isinstance(nested_data, dict):
        nested_data = [nested_data]

    for item in nested_data:
        for key, value in item.items():
            nested_mapping_info = lookup_dict.get(key)
            if nested_mapping_info:
                data_type = nested_mapping_info["type"]
                if data_type == "nested":
                    nested_results = normalize_nested_data(
                        value, company_id, timestamp, lookup_dict
                    )
                    normalized_results.extend(nested_results)
                else:
                    normalized_data = process_data_point(
                        value, company_id, timestamp, nested_mapping_info
                    )
                    normalized_results.append(normalized_data)
    return normalized_results


def normalize_data(
    raw_data: RawData, mapping_schema: NormalizationSchema
) -> list[NormalizedData]:
    """Normalizes raw data according to the provided mapping schema for one company at a
    time.

    Args:
    raw_data RawData: The raw data to be normalized.
    mapping_schema (dict[str, Any]): The mapping schema for normalization.

    Returns:
    list[NormalizedData]: The listof normalized data points.
    """
    lookup_dict = build_lookup_dict(mapping_schema.schema)
    normalized_results = []

    timestamp = str(raw_data.create_time)
    company_id = str(raw_data.company_id)

    data = raw_data.data
    for key, value in data.items():
        mapping_info = lookup_dict.get(key)
        if not mapping_info:
            print(f"Warning: Key '{key}' not found in lookup dictionary")
            continue

        data_type = mapping_info["type"]
        if data_type == "nested":
            nested_results = normalize_nested_data(
                value, company_id, timestamp, lookup_dict
            )
            normalized_results.extend(nested_results)
        else:
            normalized_data = process_data_point(
                value, company_id, timestamp, mapping_info
            )
            normalized_results.append(normalized_data)
    return normalized_results