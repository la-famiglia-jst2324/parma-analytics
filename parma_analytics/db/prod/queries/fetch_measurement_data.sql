SELECT
    company_measurement_id,
    value,
    created_at
FROM measurement_table
WHERE company_measurement_id IN :measurement_ids
ORDER BY company_measurement_id, created_at;
