SELECT
    id,
    type,
    measurement_name,
    source_module_id,
    parent_measurement_id,
    created_at,
    modified_at
FROM source_measurement WHERE id =: id
