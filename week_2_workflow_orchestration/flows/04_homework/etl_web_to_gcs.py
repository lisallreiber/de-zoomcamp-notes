from pathlib import Path                            # standard libary to deal with file paths
from pandas import pandas as pd                     # popular lib to work with data
from prefect import flow, task                      # to create a flow and tasks
from prefect.tasks import task_input_hash           # to create a cache key 
from datetime import timedelta                      # to set cache expiration
from prefect_gcp.cloud_storage import GcsBucket     # to upload to GCS

@task(name="fetch data",log_prints=True, retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def fetch(dataset_url: str) -> pd.DataFrame:
    """Fetch data from a URL into Pandas DataFrame"""

    df = pd.read_csv(dataset_url, parse_dates=[1, 2])
    return df

@task(name="clean data",log_prints=True)
def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Nothing to transform"""
    print(df.head(2))
    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
    return df

@task(name="write local",log_prints=True)
def write_local(df: pd.DataFrame, color: str, dataset_file: str) -> Path:
    """Write DataFrame to local parquet file"""
    path = Path(f"data/{color}/{dataset_file}.parquet")
    # if path doesnt exist, create path
    path.parent.mkdir(parents=True, exist_ok=True)
    # if path doesnt exist, create path with to_parquet
    print(f"writing to {path}...")
    df.to_parquet(path, compression="gzip")
    return path

@task(name="write GCS",log_prints=True)
def write_gcs(path: Path) -> None:
    """Write local parquet file to GCS"""
    gcp_cloud_storage_bucket_block = GcsBucket.load("de-zoomcamp-gcs")
    gcp_cloud_storage_bucket_block.upload_from_path(
        from_path=f"{path}",
        to_path=path,
        timeout=120
    )
    return

@flow(name="etl-web-to-gcs")
def etl_web_to_gcs() -> None:
    """Main ETL Function"""
    color = "yellow"
    year = 2019
    month = 3
    dataset_file = f"{color}_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"

    df = fetch(dataset_url)
    df_clean = clean(df)
    path = write_local(df_clean, color, dataset_file)
    write_gcs(path)

if __name__ == "__main__":
    etl_web_to_gcs()