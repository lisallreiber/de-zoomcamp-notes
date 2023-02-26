{{ config(materialized='table') }}

with fhv_trips as (
    select *
    from {{ ref('stg_fhv_data') }}
),

dim_zones as (
    select * from {{ ref('dim_zones') }}
    where borough != 'Unknown'
)

select 
    -- general info
    fhv_trips.affiliated_base_number,
    fhv_trips.dispatching_base_number,
    fhv_trips.sr_flag,
    -- pick-up info
    fhv_trips.pickup_locationid,
    fhv_trips.pickup_datetime,
    pickup_zone.borough as pickup_borough, 
    pickup_zone.zone as pickup_zone, 
    pickup_zone.service_zone as pickup_service_zone,
    -- drop-off info
    fhv_trips.dropoff_locationid,
    fhv_trips.dropoff_datetime, 
    dropoff_zone.borough as dropoff_borough, 
    dropoff_zone.zone as dropoff_zone,
    dropoff_zone.service_zone as dropoff_service_zone  

from fhv_trips
inner join dim_zones as pickup_zone
on fhv_trips.pickup_locationid = pickup_zone.locationid
inner join dim_zones as dropoff_zone
on fhv_trips.dropoff_locationid = dropoff_zone.locationid
