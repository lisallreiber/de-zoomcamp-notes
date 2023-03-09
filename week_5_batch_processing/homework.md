## Week 5 Homework 

In this homework we'll put what we learned about Spark in practice.

For this homework we will be using the FHVHV 2021-06 data found here. [FHVHV Data](https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhvhv/fhvhv_tripdata_2021-06.csv.gz )


### Question 1: 

**Install Spark and PySpark** 

- Install Spark
- Run PySpark
- Create a local spark session
- Execute spark.version.

What's the output?
- **3.3.2 ✅**
- ~~2.1.4~~
- ~~1.2.3~~
- ~~5.4~~

**steps:**

```bash
# login to VM
ssh de-zoomcamp

# start spark
spark-shell

# view version
spark.version
```

**answer: 3.3.2 ✅**

### Question 2: 

**HVFHW June 2021**

Read it with Spark using the same schema as we did in the lessons. We will use this dataset for all the remaining questions. Repartition it to 12 partitions and save it to parquet. What is the average size of the Parquet (ending with .parquet extension) Files that were created (in MB)? Select the answer which most closely matches.

- ~~2MB~~
- **24MB ✅**
- ~~100MB~~
- ~~250MB~~

**steps:**

- download the data with [bash script](download_fhvhv-data.sh)
- process the data with [jupyter notebook](homework.py)
  - setup spark engine
  - impprt data
  - define schema
  - write to parquet
- get size of files

```bash
# cd to the folder with the data
cd data/pq/fhvhv/2021/06/
# get info about all files with size displayed as MB
ls -l --block-size=MB
```

**answer: 25MB**

### Question 3: 

**Count records**  

How many taxi trips were there on June 15?
Consider only trips that started on June 15.

- ~~308,164~~
- ~~12,856~~
- **452,470**
- ~~50,982~~

**steps:**

```python
df.createOrReplaceTempView('fhvhv')
selected_pickups = spark.sql(
    """
    SELECT COUNT(*) as number_of_taxi_trips
    FROM fhvhv
    WHERE DATE(pickup_datetime) = '2021-06-15'
    """). \
    show()
```

**output:**

    +--------------------+
    |number_of_taxi_trips|
    +--------------------+
    |              452470|
    +--------------------+

**answer: 452,470 ✅**

### Question 4: 

**Longest trip for each day**  

Now calculate the duration for each trip.</br>
How long was the longest trip in Hours?</br>

- **66.87 Hours ✅**
- ~~243.44 Hours~~
- ~~7.68 Hours~~
- ~~3.32 Hours~~

**steps:**

```python
from pyspark.sql import functions as F

df \
    .withColumn('pickup_date', F.to_date(df.pickup_datetime)) \
    .withColumn('duration', df.dropoff_datetime.cast('long') - df.pickup_datetime.cast('long')) \
    .groupBy('pickup_date') \
    .max('duration') \
    .orderBy('max(duration)', ascending=False) \
    .limit(5) \
    .show()
```

**output:**

    +-----------+-------------+
    |pickup_date|max(duration)|
    +-----------+-------------+
    | 2021-06-25|       240764|
    | 2021-06-22|        91979|
    | 2021-06-27|        71931|
    | 2021-06-26|        65510|
    | 2021-06-23|        59281|
    +-----------+-------------+


**answer: 240764 sec -> 66.87 hours ✅**

### Question 5: 

**User Interface**

 Spark’s User Interface which shows application's dashboard runs on which local port?

- ~~80~~
- ~~443~~
- **4040 ✅**
- ~~8080~~

**answer: The default is 4040, but it increments if that port is already blocked by another session ✅**

### Question 6: 

**Most frequent pickup location zone**

Load the zone lookup data into a temp view in Spark</br>
[Zone Data](https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv)

Using the zone lookup data and the fhvhv June 2021 data, what is the name of the most frequent pickup location zone?

- ~~East Chelsea~~
- ~~Astoria~~
- ~~Union Sq~~
- **Crown Heights North ✅**

**steps**

- also see [jupyter notebook](homework.py)
- 
```python
# load zone data
zone_df = spark.read.csv('data/taxi_zone_lookup.csv', header=True)

# create temp view
zones_df.createOrReplaceTempView('zones')

# join zone data with fhvhv data group by zone and count
pickup_location_counts = spark. \
    sql(
        """
            SELECT
                pul.Zone AS pickup_zone,
                COUNT(1)
            FROM 
                fhvhv fhv LEFT JOIN zones pul ON fhv.PULocationID = pul.LocationID
            GROUP BY 
                1
            ORDER BY
                2 DESC
            LIMIT 5;
        """). \
    show()
```

**output:**

    +-------------------+--------+
    |        pickup_zone|count(1)|
    +-------------------+--------+
    |Crown Heights North|  231279|
    |       East Village|  221244|
    |        JFK Airport|  188867|
    |     Bushwick South|  187929|
    |      East New York|  186780|
    +-------------------+--------+

**answer: Crown Heights North ✅**

## Submitting the solutions

* Form for submitting: https://forms.gle/EcSvDs6vp64gcGuD8
* You can submit your homework multiple times. In this case, only the last submission will be used. 

Deadline: 06 March (Monday), 22:00 CET


## Solution

We will publish the solution here
