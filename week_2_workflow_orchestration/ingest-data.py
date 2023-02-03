#!/usr/bin/env python3.9
# coding: utf-8

# DE Zoomcamp: Upload Data to Postgres

import os                              # to run shell commands
import argparse                        # to parse arguments
import pandas as pd                    # to read csv files
from time import time                  # to measure time
from datetime import timedelta         # to set cache expiration
from sqlalchemy import create_engine   # connect to db
from prefect import flow, task         # to create a flow and tasks
from prefect.tasks import task_input_hash 
from prefect_sqlalchemy import SqlAlchemyConnector

@task(
    log_prints=True, 
    retries=3, 
    cache_key_fn=task_input_hash,
    cache_expiration=timedelta(days=1)
    )
def extract_data(url):
    # step01: download data
    # ---------------------------------

    # the backup files are gzipped, and it's important to keep the correct extension
    # for pandas to be able to open the file
    if url.endswith('.csv.gz'):
        csv_name = 'taxi_data.csv.gz'
    else:
        csv_name = 'taxi_data.csv'

    # download the data
    os.system(f"wget {url} -O {csv_name}")

    # step02: import data
    # ---------------------------------
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000, parse_dates=[1, 2])
    df = next(df_iter)

    # step03: return imported df
    # ---------------------------------
    return df

@task(log_prints=True)
def transform_data(df):
    # step01: wrangle data
    # ---------------------------------
    print(f"pre: missing passenger count: {df['passenger_count'].isin([0]).sum()}")
    df = df[df['passenger_count'] != 0]
    print(f"post: missing passenger count: {df['passenger_count'].isin([0]).sum()}")
    # step02: return data
    # ---------------------------------
    return df

@task(log_prints=True, retries=3)
def ingest_data(tbl_name, df):

    # step01: connect to postgres
    # ---------------------------------
    connection_block = SqlAlchemyConnector.load("postgres-connector")

    with connection_block.get_connection() as engine:
        # step02: writing the data into the database in batches
        # ---------------------------------
        # first batch
        df.head(n=0).to_sql(name=tbl_name, con=engine, if_exists='replace')
        df.to_sql(name=tbl_name, con=engine, if_exists='append')

@flow(name= "Subflow", log_prints=True)
def log_subflow(tbl_name: str):
    print(f"Logging subflow for {tbl_name}")

@flow(name="Ingest Flow")
def ingest_flow(tbl_name: str):
    url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2020-01.csv.gz"

    log_subflow(tbl_name)
    raw_data = extract_data(url)
    data = transform_data(raw_data)
    # pass the arguments to the main method
    ingest_data(user, password, host, port, db_name, tbl_name, data)

if __name__ == '__main__':
    ingest_flow("yellow_taxi_data")