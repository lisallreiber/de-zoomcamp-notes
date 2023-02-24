from pathlib import Path                            # standard libary to deal with file paths
from pandas import pandas as pd                     # popular lib to work with data
from prefect import flow, task                      # to create a flow and tasks
from prefect_gcp.cloud_storage import GcsBucket     # to upload to GCS
from prefect_gcp import GcpCredentials              # to authenticate to GCP


@task(name="Extract from GSC", retries=3)
def extract_from_gsc(month: int, year: int,  color: str) -> Path:
    """Download trip data from GCS"""
    print(f"Extracting {color} taxi data for {year}-{month:02}...")
    gcs_path = f"data/{color}/{color}_tripdata_{year}-{month:02}.parquet"
    gcs_bucket_block = GcsBucket.load("de-zoomcamp-gcs")
    gcs_bucket_block.get_directory(
        from_path=gcs_path,
        local_path="."
    )
    df = pd.read_parquet(gcs_path)
    return df

@task(name="Write to BigQuery", log_prints=True)
def write_bq(df: pd.DataFrame, dest_table: str):
    """Write data to BigQuery"""

    gcp_credentials_block = GcpCredentials.load("de-zoomcamp-gcp-credentials")

    df.to_gbq(
        destination_table=dest_table,
        project_id="prefect-de-zoomcamp-376713",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append",
        location="europe-west9"
    )

@flow(name="etl-gcs-to-bq", log_prints=True)
def etl_gcs_to_bq(month: int, year: int, color: str):
    """Main ETL Flow to load data into BigQuery"""
    dest_table = f"trips_data_all.{color}_trips"

    df = extract_from_gsc(month, year, color)
    print(f"total number of rows: {len(df)}")
    write_bq(df, dest_table)
    
    processed_rows = len(df)     # return the number of rows processed
    return processed_rows

@flow(name="etl-factory-flow", log_prints=True)
def etl_factory_flow(
    months: list[int] = list(range(1,13)), 
    year: int = 2019, 
    color: str = "yellow"):
    """Parent flow: factory for other flows"""
    total_rows = 0 # keep track of the total number of rows processed
    for month in months:
        # etl_gcs_to_bq.with_options(name=f"{month}").submit(month)
        processed_rows = etl_gcs_to_bq(month, year, color)
        total_rows += processed_rows  # add the number of rows processed by the child flow
    print(f"total rows processed: {total_rows}")

if __name__ == "__main__":
    months = [1]
    year = 2019
    color = "yellow"
    etl_factory_flow(months, year, color) # make sure they are in the right order
