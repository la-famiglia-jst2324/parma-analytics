INSERT INTO source_measurement (
    type, measurement_name, source_module_id, parent_measurement_id,
    created_at, modified_at
) VALUES (
    : type,: measurement_name,: source_module_id,: parent_measurement_id,
    NOW(), NOW()
) RETURNING *
