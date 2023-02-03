from pathlib import Path                            # standard libary to deal with file paths
from pandas import pandas as pd                     # popular lib to work with data
from prefect import flow, task                      # to create a flow and tasks
from prefect.tasks import task_input_hash           # to create a cache key 
from datetime import timedelta                      # to set cache expiration
from prefect_gcp.cloud_storage import GcsBucket     # to upload to GCS
from prefect_gcp import GcpCredentials              # to authenticate to GCP


@task(name="Extract from GSC", retries=3)
def extract_from_gsc(color: str, year: int, month: int) -> Path:
    """Download trip data from GCS"""
    gcs_path = f"data/{color}/{color}_tripdata_{year}-{month:02}.parquet"
    gcs_bucket_block = GcsBucket.load("de-zoomcamp-gcs")
    gcs_bucket_block.get_directory(
        from_path=gcs_path,
        local_path="."
    )
    return Path(f"{gcs_path}")

@task(name="Transform data from GSC")
def transform(path: Path) -> pd.DataFrame:
    """Transform data from GCS"""
    df = pd.read_parquet(path)
    print(f"pre: missing passenger count: {df['passenger_count'].isna().sum()}")
    # we assume that if passenger count is missing that the count was actually 0
    df["passenger_count"] = df["passenger_count"].fillna(0)
    # alternative with pandas inplace argument
    # df["passenger_count"].fillna(0, inplace=True)

    print(f"post: missing passenger count: {df['passenger_count'].isna().sum()}")

    return df

@task(name="Write to BigQuery", log_prints=True)
def write_bq(df: pd.DataFrame):
    """Write data to BigQuery"""

    gcp_credentials_block = GcpCredentials.load("de-zoomcamp-gcp-credentials")

    df.to_gbq(
        destination_table="yellow_taxi_trips.rides",
        project_id="prefect-de-zoomcamp-376713",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append"
    )


@flow(name="ETL GCS to BQ")
def etl_gcs_to_bq():
    """Main ETL Flow to load data into BigQuery"""
    color = "yellow"
    year = 2021
    month = 1

    path = extract_from_gsc(color, year, month)
    df = transform(path)
    write_bq(df)

if __name__ == "__main__":
    etl_gcs_to_bq()


    