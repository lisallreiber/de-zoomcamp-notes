from pathlib import Path   # standard libary to deal with file paths
from pandas import pandas as pd   # popular lib to work with data
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from random import randint

@task(retries=3)
def fetch(dataset_url: str) -> pd.DataFrame:
    """Fetch data from a URL into Pandas DataFrame"""
    if randint(0,1) > 0:
        raise Exception("Random Error")
        
    df = pd.read_csv(dataset_url)
    return df

@flow()
def etl_web_to_gcs() -> None:
    """Main ETL Function"""
    color = "yellow"
    year = 2020
    month = 1
    dataset_file = f"{color}_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"

    df = fetch(dataset_url)


if __name__ == "__main__":
    etl_web_to_gcs()