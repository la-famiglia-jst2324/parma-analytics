-- -------------------------------------------------------------------------------------
--                      insert scheduled_tasks for next 24 hours
-- -------------------------------------------------------------------------------------

WITH RECURSIVE last_runs_per_datasource (id, freq, last_schedule) AS (
    SELECT
        ds.id        AS id,
        ds.frequency AS freq,
        CASE
            WHEN MAX(st.scheduled_at) > NOW() THEN MAX(st.scheduled_at)
            ELSE NOW()
        END          AS last_schedule
    FROM data_source AS ds
    LEFT JOIN scheduled_task AS st ON ds.id = st.data_source_id
    -- not on_demand scheduled
    WHERE
        (st.schedule_type = 'REGULAR' OR st.schedule_type IS NULL)
        AND ds.is_active = TRUE

    GROUP BY id, freq  -- look at data sources latest regular schedules
),

next_runs_per_datasource (id, scheduled_at) AS (
    (
        SELECT
            id            AS id,
            last_schedule AS last_schedule
        FROM last_runs_per_datasource
    )
    UNION
    (
        SELECT
            nrpd.id,
            CASE
                WHEN
                    (d.frequency = 'HOURLY')
                THEN nrpd.scheduled_at + INTERVAL '1 hour'
                WHEN
                    (d.frequency = 'DAILY')
                THEN nrpd.scheduled_at + INTERVAL '1 day'
                WHEN
                    (d.frequency = 'WEEKLY')
                THEN nrpd.scheduled_at + INTERVAL '1 week'
                WHEN
                    (d.frequency = 'MONTHLY')
                THEN nrpd.scheduled_at + INTERVAL '1 month'
                ELSE nrpd.scheduled_at + INTERVAL '1 day'
            END AS scheduled_at
        FROM next_runs_per_datasource AS nrpd
        INNER JOIN data_source AS d ON nrpd.id = d.id
        WHERE nrpd.scheduled_at < NOW() + INTERVAL '1 day'
    )
),

next_runs_without_current (id, scheduled_at) AS (
    SELECT *
    FROM next_runs_per_datasource
    WHERE NOT EXISTS (
            SELECT 1
            FROM last_runs_per_datasource
            WHERE
                next_runs_per_datasource.id = last_runs_per_datasource.id
                AND next_runs_per_datasource.scheduled_at
                = last_runs_per_datasource.last_schedule
        )
)

-- insert new tasks into scheduled_task table
INSERT INTO scheduled_task (
    data_source_id, schedule_type, scheduled_at, max_run_seconds
)
SELECT
    d.id              AS data_source_id,
    'REGULAR'         AS schedule_type,
    n.scheduled_at    AS scheduled_at,
    d.max_run_seconds AS max_run_seconds
FROM next_runs_without_current AS n
INNER JOIN data_source AS d ON n.id = d.id;

-- -------------------------------------------------------------------------------------
--           drop all unfinished scheduled tasks for deactivted data_sources
-- -------------------------------------------------------------------------------------
WITH tasks_to_delete (task_id) AS (
    SELECT st.task_id
    FROM scheduled_task AS st
    INNER JOIN data_source AS ds ON st.data_source_id = ds.id
    WHERE
        st.status = 'PENDING' -- unstarted tasks
        AND st.schedule_type = 'REGULAR' -- not on_demand tasks
        AND ds.is_active = FALSE
)

DELETE FROM scheduled_task st
WHERE st.task_id IN (SELECT task_id FROM tasks_to_delete)
