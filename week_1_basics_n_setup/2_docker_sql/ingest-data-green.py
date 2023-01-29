#!/usr/bin/env python
# coding: utf-8

# DE Zoomcamp: Upload Green Taxi data to Postgres

import os
import argparse
import pandas as pd

from time import time
from sqlalchemy import create_engine # to help with named arguments


def main(params):
    # unpack params
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db_name = params.db_name
    tbl_name = params.tbl_name
    url = params.url

    # the backup files are gzipped, and it's important to keep the correct extension
    # for pandas to be able to open the file
    if url.endswith('.csv.gz'):
        csv_name = 'taxi_data.csv.gz'
    else:
        csv_name = 'taxi_data.csv'

    # step01: download data
    # ----------------------------
    print(f'step01 - download data into {csv_name}: start...')

    os.system(f"wget {url} -O {csv_name}")

    print(f'step1 - download data into {csv_name}: finished')

    # step02: import data
    print(f'step02 - wrangle data: start...')

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)
    df = next(df_iter)

    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
    
    print(f'step02 - wrangle data: finished')

    # step02: connect to postgres
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')

    # step03: writing the data into the databas in batches
    print(f'step03 - ingest data into postgres: start...')
    # first batch
    df.head(n=0).to_sql(name=tbl_name, con=engine, if_exists='replace')
    df.to_sql(name=tbl_name, con=engine, if_exists='append')

    # all other batches
    while True:

        try:
            t_start = time()

            df = next(df_iter)

            df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
            df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

            df.to_sql(name=tbl_name, con=engine, if_exists='append')

            t_end = time()

            print('inserted another chunk, took %.3f seconds' % (t_end - t_start))

        except StopIteration:
            print("step03 - ingest data into postgres: finished")
            break

if __name__ == '__main__':

    # parse all the arguments
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db_name', required=True, help='database name for postgres')
    parser.add_argument('--tbl_name', required=True, help='table name for postgres')
    parser.add_argument('--url', required=True, help='url of the csv file')

    args = parser.parse_args()

    # pass the arguments to the main method
    main(args)



