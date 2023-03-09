#!/usr/bin/env python
# coding: utf-8

# In[16]:
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import types
import pandas as pd


# In[2]:


# main entrypoint to spark / object we use to interact with spark
spark = SparkSession.builder \
    .master("local[*]") \
    .appName('test') \
    .getOrCreate()


# ## Download data
# 
# as a first step we will download that FHVHV Data for June 2021 from the Link provided in the homework instructions.

# In[4]:


# download data
# ! download_fhvhv-data.sh 2021 6


# ## Explore Data
# 
# 

# In[3]:


# how many lines does the file have?
get_ipython().system('zcat "../data/raw/fhvhv/2021/06/fhvhv_tripdata_2021_06.csv.gz" | wc -l')


# In[4]:


get_ipython().system('zcat "../data/raw/fhvhv/2021/06/fhvhv_tripdata_2021_06.csv.gz" | head -n 5')


# In[5]:


# read as sparf df
df = spark.read \
    .options(header = "true", inferSchema = "true") \
    .csv('../data/raw/fhvhv/2021/06/fhvhv_tripdata_2021_06.csv.gz')


# In[65]:


df.show(5)


# In[6]:


# df.Schema()
df.printSchema()


# ## Construct Schema
# 
# - we use pandas to infer types and then use types to create schema in local DB

# In[48]:


# step1: write out a mini subset with linux commands
get_ipython().system('zcat "../data/raw/fhvhv/2021/06/fhvhv_tripdata_2021_06.csv.gz" | head -n 102 > head.csv')


# In[69]:


# take a look at head
get_ipython().system('head -n 10 head.csv')


# In[70]:


get_ipython().system('wc -l head.csv')


# In[18]:


# import as pandas df
# df_pandas = pd.read_csv('head.csv')
# df_pandas
# df_pandas.dtypes
# df_spark = spark.createDataFrame(df_pandas[df_pandas.notnull().all(1)])
# df_spark.schema


# In[23]:


schema_fhvhv = types.StructType([
    types.StructField('dispatching_base_num',types.StringType(),True),
    types.StructField('pickup_datetime',types.TimestampType(),True),
    types.StructField('dropoff_datetime',types.TimestampType(),True),
    types.StructField('PULocationID',types.IntegerType(),True),
    types.StructField('DOLocationID',types.IntegerType(),True),
    types.StructField('SR_Flag',types.DoubleType(),True),
    types.StructField('Affiliated_base_number',types.StringType(),True)
])


# In[24]:


df = spark.read \
    .option("header", "true") \
    .schema(schema_fhvhv) \
    .csv('../data/raw/fhvhv/2021/06/fhvhv_tripdata_2021_06.csv.gz')


# In[25]:


df.show()


# ## Repartition to 12 partitions

# In[27]:


df = df.repartition(12)


# ## Export to parquet

# In[28]:


# specify mode='overwrite' to overwrite
df.write.parquet('../data/pq/fhvhv/2021/06', mode='overwrite')


# In[29]:


df = spark.read.parquet('../data/pq/fhvhv/2021/06')


# In[30]:


df.printSchema()


# In[ ]:




