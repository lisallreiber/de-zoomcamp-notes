## Week 4 Homework 

In this homework, we'll use the models developed during the week 4 videos and enhance the already presented dbt project using the already loaded Taxi data for fhv vehicles for year 2019 in our DWH.

This means that in this homework we use the following data [Datasets list](https://github.com/DataTalksClub/nyc-tlc-data/)
* Yellow taxi data - Years 2019 and 2020 ✅
* Green taxi data - Years 2019 and 2020 ✅
* fhv data - Year 2019. ✅

We will use the data loaded for:

* Building a source table: `stg_fhv_tripdata`
* Building a fact table: `fact_fhv_trips`
* Create a dashboard 

If you don't have access to GCP, you can do this locally using the ingested data from your Postgres database
instead. If you have access to GCP, you don't need to do it for local Postgres -
only if you want to.

> **Note**: if your answer doesn't match exactly, select the closest option 

### Question 1: 

**What is the count of records in the model fact_trips after running all models with the test run variable disabled and filtering for 2019 and 2020 data only (pickup datetime)?** 

You'll need to have completed the ["Build the first dbt models"](https://www.youtube.com/watch?v=UVI30Vxzd6c) video and have been able to run the models via the CLI. 
You should find the views and models for querying in your DWH.

- ~~41648442~~
- ~~51648442~~
- **✅ 61648442**
- ~~71648442~~

**steps:**
1. setup prefect [flows](flows/taxi-flow-factory_gcs-to-bq.py) to load the taxi rides data for 2019 and 2020 into BigQuery
2. setup a [dbt project](ny_taxi_rides_project/dbt_project.yml) and build the models for fact_trips and dim_zones


**my answer: 61541864 ✅**


### Question 2: 

**What is the distribution between service type filtering by years 2019 and 2020 data as done in the videos?**

You will need to complete "Visualising the data" videos, either using [google data studio](https://www.youtube.com/watch?v=39nLTs74A3E) or [metabase](https://www.youtube.com/watch?v=BnLkrA7a6gM). 

- **89.9/10.1**
- ~~94/6~~
- ~~76.3/23.7~~
- ~~99.1/0.9~~

**steps:**

1. open a [Google Looker Report](https://lookerstudio.google.com/reporting/c6e2f62d-8d0d-456c-8b57-501769a13f96) and visualize the distribution of service types with a donut 

**my answer: Yellow: 89.8 % / Green: 10.2 % ✅**

### Question 3: 

**What is the count of records in the model stg_fhv_tripdata after running all models with the test run variable disabled (:false)?**  

Create a staging model for the fhv data for 2019 and do not add a deduplication step. Run it via the CLI without limits (is_test_run: false).
Filter records with pickup time in year 2019.

- ~~33244696~~
- ✅ 43244696
- ~~53244696~~
- ~~63244696~~

**steps:**

1. Create a staging model for the fhv data for 2019 without a deduplication step und run a build job with dbt.

- adapt the schema.yml
- build a stg_fhv model
```
dbt run --select stg_fhv_data --var 'is_test_run: false'
```

- run BigQuery query to check the count of records in the model stg_fhv_tripdata
```sql
SELECT count(*)
FROM `prefect-de-zoomcamp-376713.dbt_lreiber_models.stg_fhv_data`
WHERE EXTRACT(YEAR from pickup_datetime) in (2019)
```

**my answer: 43244696 ✅**

### Question 4: 

**What is the count of records in the model fact_fhv_trips after running all dependencies with the test run variable disabled (:false)?**  

Create a core model for the `stg_fhv_tripdata` joining with `dim_zones`.
Similar to what we've done in `fact_trips`, keep only records with known pickup and dropoff locations entries for pickup and dropoff locations. 
Run it via the CLI without limits (is_test_run: false) and filter records with pickup time in year 2019.

- ~~12998722~~
- **✅ 22998722**
- ~~32998722~~
- ~~42998722~~


1. Create a core model for the `stg_fhv_tripdata` joining with dim_zones.

```sql
SELECT count(*)
FROM `prefect-de-zoomcamp-376713.dbt_lreiber_models.fact_fhv_trips` 
WHERE EXTRACT(YEAR from pickup_datetime) = 2019
```


### Question 5: 

**What is the month with the biggest amount of rides after building a tile for the fact_fhv_trips table?**

Create a dashboard with some tiles that you find interesting to explore the data. One tile should show the amount of trips per month, as done in the videos for fact_trips, based on the fact_fhv_trips table.

- ~~March~~
- ~~April~~
- **✅ January**
- ~~December~~

**steps:**

1. connect the procuction facts_fhv_trips model with [Google Data Looker](https://lookerstudio.google.com/reporting/3c92be27-5fb5-4c15-a6d7-3596283f634e)
2. Generate some visualizations
   
**my answer: January ✅**

## Public Learning

- [Tweet about dbt YAML syntax](https://twitter.com/lisa_reiber/status/1628424594099929090?s=20)
- [Tweet about YAML debugging](https://twitter.com/lisa_reiber/status/1629060305522229248?s=20)
- [Tweet about .gitignore and csv files](https://twitter.com/lisa_reiber/status/1628748198801035270?s=20)
- [Tweet about DevX via cats in vscode](https://twitter.com/lisa_reiber/status/1626595506695839754?s=20)
