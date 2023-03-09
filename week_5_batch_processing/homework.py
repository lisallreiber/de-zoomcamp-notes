#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import types
from pyspark.sql import functions as F
import pandas as pd


# In[5]:


# main entrypoint to spark / object we use to interact with spark
spark = SparkSession.builder \
    .master("local[*]") \
    .appName('test') \
    .getOrCreate()


# ## Download data
# 
# as a first step we will download that FHVHV Data for June 2021 from the Link provided in the homework instructions.

# In[ ]:


# download data
# ! download_fhvhv-data.sh 2021 6


# In[6]:


get_ipython().system('wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv -O "../data/raw/taxi_zone_lookup.csv"')


# ## Explore Data
# 
# 

# ### Trip Data

# In[ ]:


# how many lines does the file have?
get_ipython().system('zcat "../data/raw/fhvhv/2021/06/fhvhv_tripdata_2021_06.csv.gz" | wc -l')


# In[ ]:


get_ipython().system('zcat "../data/raw/fhvhv/2021/06/fhvhv_tripdata_2021_06.csv.gz" | head -n 5')


# In[11]:


# read as sparf df
df = spark.read \
    .options(header = "true", inferSchema = "true") \
    .csv('../data/raw/fhvhv/2021/06/fhvhv_tripdata_2021_06.csv.gz')


# In[8]:


df.show(5)


# In[9]:


# df.Schema()
df.printSchema()


# ### Zones data

# In[12]:


zones_df = spark.read \
    .options(header = "true", inferSchema = "true") \
    .csv('../data/raw/taxi_zone_lookup.csv')


# In[15]:


zones_df.show(5)


# ## Construct Schema
# 
# - we use pandas to infer types and then use types to create schema in local DB

# In[ ]:


# step1: write out a mini subset with linux commands
get_ipython().system('zcat "../data/raw/fhvhv/2021/06/fhvhv_tripdata_2021_06.csv.gz" | head -n 102 > head.csv')


# In[ ]:


# take a look at head
get_ipython().system('head -n 10 head.csv')


# In[ ]:


get_ipython().system('wc -l head.csv')


# In[ ]:


# import as pandas df
# df_pandas = pd.read_csv('head.csv')
# df_pandas
# df_pandas.dtypes
# df_spark = spark.createDataFrame(df_pandas[df_pandas.notnull().all(1)])
# df_spark.schema


# In[ ]:


schema_fhvhv = types.StructType([
    types.StructField('dispatching_base_num',types.StringType(),True),
    types.StructField('pickup_datetime',types.TimestampType(),True),
    types.StructField('dropoff_datetime',types.TimestampType(),True),
    types.StructField('PULocationID',types.IntegerType(),True),
    types.StructField('DOLocationID',types.IntegerType(),True),
    types.StructField('SR_Flag',types.DoubleType(),True),
    types.StructField('Affiliated_base_number',types.StringType(),True)
])


# In[ ]:


df = spark.read \
    .option("header", "true") \
    .schema(schema_fhvhv) \
    .csv('../data/raw/fhvhv/2021/06/fhvhv_tripdata_2021_06.csv.gz')


# In[ ]:


df.show()


# ## Repartition to 12 partitions

# In[ ]:


df = df.repartition(12)


# ## Export to parquet

# In[ ]:


# specify mode='overwrite' to overwrite
df.write.parquet('../data/pq/fhvhv/2021/06', mode='overwrite')


# In[ ]:


df = spark.read.parquet('../data/pq/fhvhv/2021/06/*')


# In[ ]:


df.printSchema()


# ## Insights
# 
# ### How many taxi trips were there on June 15? 
# 
# Consider only trips that started on June 15.

# In[18]:


df.createOrReplaceTempView('fhvhv')


# In[19]:


selected_pickups = spark.sql(
    """
    SELECT COUNT(*) as number_of_taxi_trips
    FROM fhvhv
    WHERE DATE(pickup_datetime) = '2021-06-15'
    """). \
    show()


# ### Longest trip for each day: How long was the longest trip in Hours?
# 
# Calculate the duration for each trip. 

# In[ ]:


df \
    .withColumn('pickup_date', F.to_date(df.pickup_datetime)) \
    .withColumn('duration', df.dropoff_datetime.cast('long') - df.pickup_datetime.cast('long')) \
    .groupBy('pickup_date') \
    .max('duration') \
    .orderBy('max(duration)', ascending=False) \
    .limit(5) \
    .show()


# ### What is the name of the most frequent pickup location zone ?

# In[17]:


zones_df.createOrReplaceTempView('zones')


# In[21]:


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

