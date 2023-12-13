with recursive last_runs_per_datasource(id, freq, last_schedule) as (
	select
		ds.id id,
		ds.frequency freq,
		case
			when max(st.scheduled_at) > now() then max(st.scheduled_at)
			else now()
		end as last_schedule
	from data_source ds
	left join scheduled_task st on ds.id = st.data_source_id
	where st.schedule_type = 'REGULAR' or st.schedule_type is NULL  -- not on_demand scheduled

	group by id, freq  -- look at data sources latest regular schedules
),
-- recursive query to generate next dates
next_runs_per_datasource(id, scheduled_at) as (
	(
		select id, last_schedule from last_runs_per_datasource
	) union (
		select
			nrpd.id,
			(case
				when (d.frequency = 'HOURLY') then nrpd.scheduled_at + '1 hour'
				when (d.frequency = 'DAILY') then nrpd.scheduled_at + '1 day'
				when (d.frequency = 'WEEKLY') then nrpd.scheduled_at + '1 week'
				when (d.frequency = 'MONTHLY') then nrpd.scheduled_at + '1 month'
			else nrpd.scheduled_at + '1 day' end) as scheduled_at
		from next_runs_per_datasource nrpd
			join data_source d
			on nrpd.id = d.id
		where scheduled_at < now() + '1 day'
	)
),
next_runs_without_current(id, scheduled_at) as (
	select *
	from next_runs_per_datasource n
	where not exists (
		select *
		from last_runs_per_datasource l
		where n.id = l.id and n.scheduled_at = l.last_schedule
	)
)

-- insert new tasks into scheduled_task table
insert into scheduled_task (data_source_id, schedule_type, scheduled_at, max_run_seconds)
select d.id, 'REGULAR', n.scheduled_at, d.max_run_seconds
from next_runs_without_current n
join data_source d on n.id = d.id
