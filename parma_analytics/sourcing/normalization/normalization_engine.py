from typing import Any, Dict


def build_lookup_dict(mapping_schema: Dict[str, Any]) -> Dict[str, Dict[str, str]]:
    lookup_dict = {}
    for mapping in mapping_schema["Mappings"]:
        source_field = mapping["source_field"]
        lookup_dict[source_field] = {
            "type": mapping["type"],
            "source_measurement_id": mapping["source_measurement_id"],
        }

        # Handle nested mappings
        if mapping["type"] == "nested":
            for nested_mapping in mapping.get("NestedMappings", []):
                nested_field = nested_mapping["source_field"]
                lookup_dict[nested_field] = {
                    "type": nested_mapping["type"],
                    "source_measurement_id": nested_mapping["source_measurement_id"],
                }
    return lookup_dict


def process_data_point(value, company_id, timestamp, mapping):
    normalized_data = {}

    normalized_data["source_measurement_id"] = mapping["source_measurement_id"]
    normalized_data["timeStamp"] = timestamp
    normalized_data["company_id"] = company_id
    normalized_data["value"] = value
    normalized_data["type"] = mapping["type"]

    return normalized_data


def normalize_data(raw_data, mapping_schema):
    lookup_dict = build_lookup_dict(mapping_schema)
    normalized_results = []
    for company in raw_data:
        company_id = company["company_id"]
        timestamp = company["timestamp"]
        for data in company["data"]:
            for key, value in data.items():
                mapping_info = lookup_dict[key]
                data_type = mapping_info["type"]
                if data_type == "nested":
                    if isinstance(value, list):
                        for nested_data in value:
                            for nested_key, nested_value in nested_data.items():
                                nested_mapping_info = lookup_dict[nested_key]
                                normalized_data = process_data_point(
                                    nested_value,
                                    company_id,
                                    timestamp,
                                    nested_mapping_info,
                                )
                                normalized_results.append(normalized_data)
                    else:
                        for nested_key, nested_value in value.items():
                            nested_mapping_info = lookup_dict[nested_key]
                            normalized_data = process_data_point(
                                nested_value, company_id, timestamp, nested_mapping_info
                            )
                            normalized_results.append(normalized_data)

                else:
                    normalized_data = process_data_point(
                        value, company_id, timestamp, mapping_info
                    )
                    normalized_results.append(normalized_data)

    print(normalized_results)
    return normalized_results
