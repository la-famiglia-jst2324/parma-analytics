-- dialect=postgres

SELECT
    csm.company_measurement_id,
    c.id          AS company_id,
    c.description AS company_description,
    c.name        AS company_name,
    ds.id         AS source_module_id,
    ds.source_name,
    sm.id         AS measurement_id,
    sm.measurement_name,
    sm.type       AS measurement_type
FROM company_source_measurement AS csm
INNER JOIN
    company AS c ON csm.company_id = c.id
INNER JOIN
    source_measurement AS sm ON csm.source_measurement_id = sm.id
INNER JOIN
    data_source AS ds ON sm.source_module_id = ds.id
ORDER BY
    c.id, ds.id, sm.id
