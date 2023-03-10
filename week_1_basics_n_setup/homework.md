Week 1 Homework
---
- [Docker](#docker)
  - [Question 1 - Knowing docker tags](#question-1---knowing-docker-tags)
  - [Question 2 - Understanding docker first run](#question-2---understanding-docker-first-run)
- [Postgres](#postgres)
  - [Instruction](#instruction)
  - [Set-up Process](#set-up-process)
  - [Question 3 - Count records](#question-3---count-records)
  - [Question 4 - Largest trip for each day](#question-4---largest-trip-for-each-day)
  - [Question 5 - The number of passengers](#question-5---the-number-of-passengers)
  - [Question 6 - Largest tip](#question-6---largest-tip)
- [terraform](#terraform)
  - [Instruction](#instruction-1)
  - [Question 7 - Creating Resources](#question-7---creating-resources)
  - [Submitting the solutions](#submitting-the-solutions)
- [Learning in public](#learning-in-public)


In this homework we'll prepare the environment 
and practice with Docker and SQL

# Docker

## Question 1 - Knowing docker tags

Run the command ```docker --help``` to get information on Docker.
Now run the command to **get help on the "docker build"** command

Which tag has the following text? *Write the image ID to the file* 

- ~~`--imageid string`~~
- **`--iidfile string`** ✅ 
- ~~`--idimage string`~~
- ~~`--idfile string`~~

**✅ Answer: ```--iidfile string```**


## Question 2 - Understanding docker first run 

Run docker with the **python:3.9 image** in an interactive mode and the entrypoint of bash.
Now check the python modules that are installed ( use pip list). 
How many python packages/modules are installed?

- ~~1~~
- ~~6~~
- **3** ✅ 
- ~~7~~

```bash
# run the python:3.9 image in indtc-de-375708teractive mode (-it) 
docker run -it --entrypoint=bash python:3.9

pip list
```

**✅ Answer: 3**


# Postgres

## Instruction
Run Postgres and load data as shown in the videos

We'll use the green taxi trips from January 2019:

```bash
wget -nc https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz
```

You will also need the dataset with zones:

```bash
wget -O "taxi_zone_lookup.csv" -nc https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv
```

Download this data and put it into Postgres (with jupyter notebooks or with a pipeline)

## Set-up Process

**Step1: Start Docker Network** 
with Postgres and pgAdmin defined in the [`docker-compose.yaml`](2_docker_sql/docker-compose.yaml)

```bash
docker-compose -p "pg-network" up 
```

-> go to localhost:8080 and login to pgAdmin to check on the postgres db or

```bash
# connect to postgres via pgcli
pgcli -h localhost -p 5432 -u root -d ny_taxi

# then list the tables with 
\dt
```

Output: 

| Schema | Name             | Type  | Owner |
|--------|------------------|-------|-------|
| public | yellow_taxi_data | table | root  |
| public | zones            | table | root  |

**Goal:** add green_taxi_data

**Step2: Download the data**

I add the -nc flag to prevent downloading the data again if it's already present

```bash
wget -nc https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz
```

```bash
wget -O "taxi_zone_lookup.csv" -nc https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv
```

**Step3: Open jupyter notebook** to check out the new dataset and test if we can use the same pipeline just with different parameters ([Link here](2_docker_sql/ingest-data_green-taxi.ipynb))

e.g. make sure that the data cleaning steps and column names are the same

Dataset:

* https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page
* https://www1.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_green.pdf

:warning: by looking at the data dictionary we notice that some relevant column names have changed

yellow data:
![](../images/Screenshot%202023-01-26%20at%2011.53.08.png)

green data:
![](../images/Screenshot%202023-01-26%20at%2011.55.42.png)

```bash
jupyter notebook 
```

we have multiple options to deal with the new column names:
- ✅ use a [jupyter notebook](2_docker_sql/ingest-data_green-taxi.ipynb) to add the green taxi data
- add an if else statement into the existing ingest-data.py that depends on thew tbl_name parameter (green_taxi vs yellow_taxi)
- add a [ingest-data-green.py](2_docker_sql/ingest-data-green.py) script, adapt the [Dockerfile](2_docker_sql/Dockerfile) and build an image with:
  
```bash
docker build -t ingest_taxi-data-green:v001 . 
```

and 

```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz"

docker run -it \
--name=ingest-taxi-data-green \
--network=pg-network \
    ingest_taxi-data-green:v001 \
    --user=root \
    --password=root \
    --host=pg-database \
    --port=5432 \
    --db_name=ny_taxi \
    --tbl_name=green_taxi_data \
    --url=${URL} 
```

## Question 3 - Count records 

How many taxi trips were totally made on January 15?

Tip: started and finished on 2019-01-15. 

Remember that `lpep_pickup_datetime` and `lpep_dropoff_datetime` columns are in the format timestamp (date and hour+min+sec) and not in date.

- ~~20689~~
- 20530 ✅
- ~~17630~~
- ~~21090~~

**query:**
```sql
SELECT
  COUNT(1) as total_trips,
  ROUND(SUM(total_amount)) AS total_amount,
  SUM(passenger_count) AS total_passengers
FROM
  green_taxi_data
WHERE 
  date(lpep_pickup_datetime)='2019-01-15' AND
  date(lpep_dropoff_datetime)='2019-01-15'
GROUP BY date(lpep_dropoff_datetime);
```

**output:**

| total_trips | total_amount | total_passengers |
|-------------|--------------|------------------|
| 20530       | 343848.0     | 26762            |

**✅ answer: 20530**

## Question 4 - Largest trip for each day

Which was the day with the largest trip distance
Use the pick up time for your calculations.

- ~~2019-01-18~~
- ~~2019-01-28~~
- **2019-01-15 ✅**
- ~~2019-01-10~~

**query:**
```sql
SELECT
  date(lpep_pickup_datetime) AS pickup_date,
  COUNT(1) as total_trips,
  MAX(trip_distance) AS max_distance
FROM
  green_taxi_data
GROUP BY date(lpep_pickup_datetime)
-- order max distances to the top
ORDER BY "max_distance" DESC
-- only query top 5
LIMIT 5;
```

**output:**

| pickup_date    | total_trips | max_distance |
| -------------- | ----------- | ------------ |
| **2019-01-15** | **20689**   | **117.99**   |
| 2019-01-18     | 22504       | 80.96        |
| 2019-01-28     | 20342       | 64.27        |
| 2019-01-10     | 23038       | 64.2         |
| 2019-01-06     | 17799       | 60.91        |

**✅ answer: 2019-01-15**

## Question 5 - The number of passengers

In 2019-01-01 how many trips had 2 and 3 passengers?
 
- ~~2: 1282 ; 3: 266~~
- ~~2: 1532 ; 3: 126~~
- **2: 1282 ; 3: 254 ✅**
- ~~2: 1282 ; 3: 274~~

**query:**
```sql
SELECT
  date(lpep_pickup_datetime) AS pickup_datetime,
  passenger_count, 
  COUNT(1) AS total_passengers
FROM
  green_taxi_data
WHERE 
  date(lpep_pickup_datetime)='2019-01-01' 
GROUP BY 
  1,2;
```

**output:**

| pickup_datetime | passenger_count | total_passengers |
| --------------- | --------------- | ---------------- |
| 2019-01-01      | 0               | 21               |
| 2019-01-01      | 1               | 12415            |
| **2019-01-01**  | **2**           | **1282**         |
| **2019-01-01**  | **3**           | **254**          |
| 2019-01-01      | 4               | 129              |
| 2019-01-01      | 5               | 616              |
| 2019-01-01      | 6               | 273              |

**✅ answer: 2: 1282 ; 3: 254**

## Question 6 - Largest tip

For the passengers picked up in the Astoria Zone which was the drop off zone that had the largest tip?
We want the name of the zone, not the id.

Note: it's not a typo, it's `tip` , not `trip`

- ~~Central Park~~
- ~~Jamaica~~
- ~~South Ozone Park~~
- **Long Island City/Queens Plaza ✅**

**query:**
```sql
-- this outer query does the aggregation by dropoff zone and ordering by max_tip amount
SELECT DISTINCT 
    pickup_zone, 
    dropoff_zone, 
    MAX(tip_amount) OVER (PARTITION BY dropoff_zone) AS max_tip
FROM (
    -- this inner query does the joining and filtering and simple col names
    SELECT 
        green_taxi_data.tip_amount, 
        zones_pickup."Zone" AS pickup_zone, 
        zones_dropoff."Zone" AS dropoff_zone
    FROM green_taxi_data 
    JOIN zones "zones_pickup" 
        ON green_taxi_data."PULocationID" = zones_pickup."LocationID"
    JOIN zones "zones_dropoff" 
        ON green_taxi_data."DOLocationID" = zones_dropoff."LocationID"
    WHERE zones_pickup."Zone" = 'Astoria'
) astoria_taxi_trips_zones
ORDER BY "max_tip" DESC
LIMIT 5;
```

**output:**
| pickup_zone | dropoff_zone                      | max_tip  |
| ----------- | --------------------------------- | -------- |
| **Astoria** | **Long Island City/Queens Plaza** | **88.0** |
| Astoria     | Central Park                      | 30.0     |
| Astoria     | Jamaica                           | 25.0     |
| Astoria     | <null>                            | 25.0     |
| Astoria     | Astoria                           | 18.16    |

**✅ answer: Long Island City/Queens Plaza**

# terraform

## Instruction

- In this homework we'll prepare the environment by creating resources in GCP with Terraform.
- In your VM on GCP install Terraform. Copy the files from the course repo here to your VM.
- Modify the files as necessary to create a GCP Bucket and Big Query Dataset.

## Question 7 - Creating Resources
After updating the `main.tf` and `variable.tf` files run: `terraform apply`
Paste the output of this command into the homework submission form.

command:
```sh
# connect to the VM via external IP adress
ssh de-zoomcamp

# after terraform init and plan, run apply
terraform apply 
```

output:

```bash
Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # google_bigquery_dataset.dataset will be created
  + resource "google_bigquery_dataset" "dataset" {
      + creation_time              = (known after apply)
      + dataset_id                 = "trips_data_all"
      + delete_contents_on_destroy = false
      + etag                       = (known after apply)
      + id                         = (known after apply)
      + labels                     = (known after apply)
      + last_modified_time         = (known after apply)
      + location                   = "europe-west9"
      + project                    = "dtc-de-375708"
      + self_link                  = (known after apply)

      + access {
          + domain         = (known after apply)
          + group_by_email = (known after apply)
          + role           = (known after apply)
          + special_group  = (known after apply)
          + user_by_email  = (known after apply)

          + dataset {
              + target_types = (known after apply)

              + dataset {
                  + dataset_id = (known after apply)
                  + project_id = (known after apply)
                }
            }

          + routine {
              + dataset_id = (known after apply)
              + project_id = (known after apply)
              + routine_id = (known after apply)
            }

          + view {
              + dataset_id = (known after apply)
              + project_id = (known after apply)
              + table_id   = (known after apply)
            }
        }
    }

  # google_storage_bucket.data-lake-bucket will be created
  + resource "google_storage_bucket" "data-lake-bucket" {
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "EUROPE-WEST9"
      + name                        = "dtc_data_lake_dtc-de-375708"
      + project                     = (known after apply)
      + public_access_prevention    = (known after apply)
      + self_link                   = (known after apply)
      + storage_class               = "STANDARD"
      + uniform_bucket_level_access = true
      + url                         = (known after apply)

      + lifecycle_rule {
          + action {
              + type = "Delete"
            }

          + condition {
              + age                   = 30
              + matches_prefix        = []
              + matches_storage_class = []
              + matches_suffix        = []
              + with_state            = (known after apply)
            }
        }

      + versioning {
          + enabled = true
        }

      + website {
          + main_page_suffix = (known after apply)
          + not_found_page   = (known after apply)
        }
    }

Plan: 2 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

google_bigquery_dataset.dataset: Creating...
google_storage_bucket.data-lake-bucket: Creating...
google_storage_bucket.data-lake-bucket: Creation complete after 1s [id=dtc_data_lake_dtc-de-375708]
google_bigquery_dataset.dataset: Creation complete after 2s [id=projects/dtc-de-375708/datasets/trips_data_all]
```

## Submitting the solutions
* Form for submitting: [form](https://forms.gle/EjphSkR1b3nsdojv7)

# Learning in public
- [Twitter Post](https://twitter.com/lisa_reiber/status/1615315121521446912?s=20&t=h33YDcE2plJyL1PYg4hBEQ)
- [Twitter: Learning](https://twitter.com/lisa_reiber/status/1616548589672464388?s=20&t=h33YDcE2plJyL1PYg4hBEQ)
