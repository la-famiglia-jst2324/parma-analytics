from datetime import datetime
from typing import Any

from parma_analytics.db.mining.models import RawData, NormalizaionSchema
from parma_analytics.sourcing.normalization.normalization_model import NormalizedData


def build_lookup_dict(mapping_schema: NormalizaionSchema) -> dict[str, dict[str, str]]:
    """Constructs a lookup dictionary from a mapping schema.

    Args:
    mapping_schema (dict[str, Any]): The mapping schema containing the fields and their types.

    Returns:
    dict[str, dict[str, str]]: A dictionary for looking up the types and source measurement IDs by source field.
    """
    lookup_dict = {}
    try:
        for mapping in mapping_schema.get("Mappings", []):
            source_field = mapping.get("source_field")
            if source_field:
                lookup_dict[source_field] = {
                    "type": mapping.get("type"),
                    "source_measurement_id": mapping.get("source_measurement_id"),
                }

                # Handle nested mappings
                if mapping.get("type") == "nested":
                    for nested_mapping in mapping.get("NestedMappings", []):
                        nested_field = nested_mapping.get("source_field")
                        if nested_field:
                            lookup_dict[nested_field] = {
                                "type": nested_mapping.get("type"),
                                "source_measurement_id": nested_mapping.get(
                                    "source_measurement_id"
                                ),
                            }
    except KeyError as e:
        print(f"Error processing mapping schema: missing key {e}")
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


def normalize_data(
    raw_data: RawData, mapping_schema: NormalizaionSchema
) -> list[NormalizedData]:
    """Normalizes raw data according to the provided mapping schema for one company at a
    time.

    Args:
    raw_data (dict[str, Any]): The raw data to be normalized.
    mapping_schema (dict[str, Any]): The mapping schema for normalization.

    Returns:
    list[NormalizedData]: The listof normalized data points.
    """
    lookup_dict = build_lookup_dict(mapping_schema)
    normalized_results = []

    company_id = str(raw_data.get("company_id", ""))
    timestamp = str(raw_data.get("timestamp", ""))

    for data_item in raw_data.get("data", []):
        for key, value in data_item.items():
            mapping_info = lookup_dict.get(key)
            if not mapping_info:
                print(f"Warning: Key '{key}' not found in lookup dictionary")
                continue

            data_type = mapping_info["type"]
            if data_type == "nested":
                nested_values = value if isinstance(value, list) else [value]
                for nested_data in nested_values:
                    for nested_key, nested_value in nested_data.items():
                        nested_mapping_info = lookup_dict.get(nested_key)
                        if nested_mapping_info:
                            normalized_data = process_data_point(
                                nested_value,
                                company_id,
                                timestamp,
                                nested_mapping_info,
                            )
                            normalized_results.append(normalized_data)
            else:
                normalized_data = process_data_point(
                    value, company_id, timestamp, mapping_info
                )
                normalized_results.append(normalized_data)
    return normalized_results
