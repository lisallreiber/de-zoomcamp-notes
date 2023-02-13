from pathlib import Path                            # standard libary to deal with file paths
from pandas import pandas as pd                     # popular lib to work with data
from prefect import flow, task                      # to create a flow and tasks
from prefect_gcp.cloud_storage import GcsBucket     # to upload to GCS
import os                                           # to run shell commands

@task(name="fetch fhv data", log_prints=True, retries=1)
def fetch(dataset_url: str) -> pd.DataFrame:
    """Fetch fhv data and fix dtype issues from a URL into Pandas DataFrame"""
    
    print(f"read from: {dataset_url}")
    df_processed = pd.read_csv(dataset_url, parse_dates=[1,2])

    print(df_processed.head(2))
    print(f"columns: {df_processed.dtypes}")
    print(f"rows: {len(df_processed)}")

    return df_processed

@task(name="write local gz.csv",log_prints=True)
def write_local(df: pd.DataFrame, dataset_file: str) -> Path:
    """Write DataFrame to local gz.csv file"""
    path = Path(f"data/fhv/{dataset_file}.csv.gz")
    path.parent.mkdir(parents=True, exist_ok=True) # if path doesnt exist, create path
    print(f"writing to {path}...")
    print(path.cwd().parent)
    # wrtie to csv if file does not exist yet
    df.to_csv(f"{path}", compression="gzip", index=False)
    return path

@task(name="write GCS",log_prints=True)
def write_gcs(path: Path) -> None:
    """Write local parquet file to GCS"""
    gcp_cloud_storage_bucket_block = GcsBucket.load("de-zoomcamp-gcs")
    gcp_cloud_storage_bucket_block.upload_from_path(
        from_path=f"{path}",
        to_path=path,
        timeout=240  
    )
    return

@task(name="remove local data",log_prints=True)
def remove_local(path: Path) -> None:
    """remove local csv file """
    os.remove(path)
    return


@flow(name="ETL Web to GCS") 
def etl_web_to_gcs(year: int, month: int) -> None:
    """Main ETL Function"""
    dataset_file = f"fhv_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/{dataset_file}.csv.gz"
    df_processed = fetch(dataset_url)
    path = write_local(df_processed, dataset_file)
    print(path)
    write_gcs(path)
    remove_local(path)

@flow()
def etl_factory_flow(
    months: list[int] = [1,2,3,4], year: int = 2019
):
    """Factory Flow"""
    for month in months:
        etl_web_to_gcs(year, month)

if __name__ == "__main__":
    months = list(range(1,2))
    year = 2019
    etl_factory_flow(months, year)