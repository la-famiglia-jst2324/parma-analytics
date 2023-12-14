with recursive last_runs_per_datasource (id, freq, last_schedule) as (
    select
        ds.id as id,
        ds.frequency as freq,
        case
            when max(st.scheduled_at) > now() then max(st.scheduled_at)
            else now()
        end as last_schedule
    from data_source as ds
    left join scheduled_task as st on ds.id = st.data_source_id
    -- not on_demand scheduled
    where st.schedule_type = 'REGULAR' or st.schedule_type is NULL

    group by id, freq  -- look at data sources latest regular schedules
),

next_runs_per_datasource (id, scheduled_at) as (
    (
        select
            id as id,
            last_schedule as last_schedule
        from last_runs_per_datasource
    )
    union
    (
        select
            nrpd.id,
            case
                when
                    (d.frequency = 'HOURLY')
                    then nrpd.scheduled_at + interval '1 hour'
                when
                    (d.frequency = 'DAILY')
                    then nrpd.scheduled_at + interval '1 day'
                when
                    (d.frequency = 'WEEKLY')
                    then nrpd.scheduled_at + interval '1 week'
                when
                    (d.frequency = 'MONTHLY')
                    then nrpd.scheduled_at + interval '1 month'
                else nrpd.scheduled_at + interval '1 day'
            end as scheduled_at
        from next_runs_per_datasource as nrpd
        inner join data_source as d on nrpd.id = d.id
        where nrpd.scheduled_at < now() + interval '1 day'
    )
),

next_runs_without_current (id, scheduled_at) as (
    select *
    from next_runs_per_datasource
    where not exists (
        select 1
        from last_runs_per_datasource
        where
            next_runs_per_datasource.id = last_runs_per_datasource.id
            and next_runs_per_datasource.scheduled_at
            = last_runs_per_datasource.last_schedule
    )
)

-- insert new tasks into scheduled_task table
insert into scheduled_task (
    data_source_id, schedule_type, scheduled_at, max_run_seconds
)
select
    d.id as data_source_id,
    'REGULAR' as schedule_type,
    n.scheduled_at as scheduled_at,
    d.max_run_seconds as max_run_seconds
from next_runs_without_current as n
inner join data_source as d on n.id = d.id;
