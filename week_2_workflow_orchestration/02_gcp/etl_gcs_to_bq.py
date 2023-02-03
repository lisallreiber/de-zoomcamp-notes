from pathlib import Path                            # standard libary to deal with file paths
from pandas import pandas as pd                     # popular lib to work with data
from prefect import flow, task                      # to create a flow and tasks
from prefect.tasks import task_input_hash           # to create a cache key 
from datetime import timedelta                      # to set cache expiration
from prefect_gcp.cloud_storage import GcsBucket     # to upload to GCS
from prefect_gcp import GcpCredentials              # to authenticate to GCP


@task(name="Extract from GSC")
def extract_from_gsc(color: str, year: int, month: int) -> Path:
    """Download trip data from GCS"""
    gcs_path = f"data/{color}/{color}_tripdata_{year}-{month:02}.parquet"
    gcs_bucket_block = GcsBucket.load("de-zoomcamp-gcs")
    gcs_bucket_block.get_directory(
        from_path=gcs_path,
        local_path="."
    )
    return Path(f"{gcs_path}")


@flow(name="ETL GCS to BQ")
def etl_gcs_to_bq():
    """Main ETL Flow to load data into BigQuery"""
    color = "yellow"
    year = 2021
    month = 1

    path = extract_from_gsc(color, year, month)

if __name__ == "__main__":
    etl_gcs_to_bq()


    