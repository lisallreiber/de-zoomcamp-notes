Week 1 Homework
---
- [Docker](#docker)
  - [Question 1 - Knowing docker tags](#question-1---knowing-docker-tags)
  - [Question 2 - Understanding docker first run](#question-2---understanding-docker-first-run)
- [Postgres](#postgres)
  - [Instruction](#instruction)
  - [Set-up Process:](#set-up-process)
  - [Question 3 - Count records](#question-3---count-records)
  - [Question 4. Largest trip for each day](#question-4-largest-trip-for-each-day)
  - [Question 5. The number of passengers](#question-5-the-number-of-passengers)
  - [Question 6. Largest tip](#question-6-largest-tip)
  - [Submitting the solutions](#submitting-the-solutions)
  - [Solution](#solution)


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

✅ Answer: ```--iidfile string```


## Question 2 - Understanding docker first run 

Run docker with the **python:3.9 image** in an interactive mode and the entrypoint of bash.
Now check the python modules that are installed ( use pip list). 
How many python packages/modules are installed?

- ~~1~~
- ~~6~~
- **3** ✅ 
- ~~7~~

Answer: 3 ✅ 

```bash
# run the python:3.9 image in indtc-de-375708teractive mode (-it) 
docker run -it --entrypoint=bash python:3.9

pip list
```


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

## Set-up Process:

**Step1: Start Docker Network** 
with Postgres and pgAdmin defined in the `docker-compose.yaml`

```bash
docker-compose -p"pg-network" up 
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

**Step3: Open jupyter notebook** to check out the new dataset and test if we can use the same pipeline just with different parameters

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
- use a jupyter notebook to add the green taxi data ✅
- add an if else statement into the existing ingest-data.py that depends on thew tbl_name parameter (green_taxi vs yellow_taxi)
- add a [ingest-data-green.py](2_docker_sql/ingest-data-green.py) script, adapt the [Dockerfile](2_docker_sql/Dockerfile) build an image with this one
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

- 20689
- 20530
- 17630
- 21090

## Question 4. Largest trip for each day

Which was the day with the largest trip distance
Use the pick up time for your calculations.

- 2019-01-18
- 2019-01-28
- 2019-01-15
- 2019-01-10

## Question 5. The number of passengers

In 2019-01-01 how many trips had 2 and 3 passengers?
 
- 2: 1282 ; 3: 266
- 2: 1532 ; 3: 126
- 2: 1282 ; 3: 254
- 2: 1282 ; 3: 274


## Question 6. Largest tip

For the passengers picked up in the Astoria Zone which was the drop off zone that had the largest tip?
We want the name of the zone, not the id.

Note: it's not a typo, it's `tip` , not `trip`

- Central Park
- Jamaica
- South Ozone Park
- Long Island City/Queens Plaza


## Submitting the solutions

* Form for submitting: [form](https://forms.gle/EjphSkR1b3nsdojv7)
* You can submit your homework multiple times. In this case, only the last submission will be used. 

Deadline: 26 January (Thursday), 22:00 CET


## Solution

We will publish the solution here
