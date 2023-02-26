-- view bc in staging area we don't want to refresh tables all the time
{{ config(materialized='view') }}

select 
    -- identifiers
    Affiliated_base_number as affiliated_base_number,
    dispatching_base_num as dispatching_base_number,
    cast(PUlocationID as integer) as  pickup_locationid,
    cast(DOlocationID as integer) as dropoff_locationid,
    
    -- timestamps
    pickup_datetime,
    dropOff_datetime as dropoff_datetime,

    --trip info
    SR_flag as sr_flag

from {{ source('staging_fhv','fhv_data_partitioned_clustered') }}


-- dbt build -n <model.sql> --var 'is_test_run: false'
{% if var('is_test_run', default=true) %}

    limit 100

{% endif%}