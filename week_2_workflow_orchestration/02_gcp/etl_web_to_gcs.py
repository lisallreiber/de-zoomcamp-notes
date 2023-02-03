from pathlib import Path   # standard libary to deal with file paths
from pandas import pandas as pd   # popular lib to work with data
from prefect import flow, task
from prefect_gcp.coud_storage import GcsBucket

@flow()
def etl_web_to_gcs() -> None:
    """Main ETL Function"""
    color = "yellow"
    year = 2021
    month = 1
    dataset_file = f"{color}_tripdata_{year}-{month:02}"
    dataset_url = "https://github.com/DataTalksClub/nyc-taxi-data/releases/download/{color}/{dataset_file}.csv.gz"

    df = fetch(dataset_url)


if __name__ == "__main__":
    etl_web_to_gcs()