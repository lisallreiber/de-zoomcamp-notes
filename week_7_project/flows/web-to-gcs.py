from pathlib import Path                            # standard libary to deal with file paths
from pandas import pandas as pd                     # popular lib to work with data
from prefect import flow, task                      # to create a flow and tasks
# import datetime as dt
# from prefect_gcp.cloud_storage import GcsBucket     # to upload to GCS
import os

@task(name="download data", log_prints=True, retries=3)
def fetch(dataset_url: str) -> pd.DataFrame:
    """Download data from a URL into Pandas DataFrame"""
    
    df = pd.read_csv(
        dataset_url,
        encoding='latin-1',
        parse_dates=['ANGELEGT_AM', 'TATZEIT_ANFANG_DATUM', 'TATZEIT_ENDE_DATUM'],
        dayfirst=True
    )
    
    return df

@task(name="clean data",log_prints=True)
def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Fix dtype issues"""
    # combine TATZEIT_DATUM and TATZEIT_STUNDE to create TATZEIT
    df['TATZEIT_ANFANG'] = df['TATZEIT_ANFANG_DATUM'] + pd.to_timedelta(df['TATZEIT_ANFANG_STUNDE'], unit='h')
    df['TATZEIT_ENDE'] = df['TATZEIT_ENDE_DATUM'] + pd.to_timedelta(df['TATZEIT_ENDE_STUNDE'], unit='h')

    # extract hour from TATZEIT_ANFANG and assign it to TATZEIT_ANFANG_STUNDE
    df['TATZEIT_ANFANG_STUNDE'] = df['TATZEIT_ANFANG'].dt.hour
    df['TATZEIT_ENDE_STUNDE'] = df['TATZEIT_ENDE'].dt.hour

    # generate tatzeit dauer
    df['TATZEIT_DAUER'] = (df['TATZEIT_ENDE'] - df['TATZEIT_ANFANG']) / pd.Timedelta(hours=1)

    print(df.head(2))
    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
    return df

@task(name="write local",log_prints=True)
def write_local(df: pd.DataFrame, dataset_file: str) -> Path:
    """Write DataFrame to local parquet file"""
    path = Path(f"data/pq/{dataset_file}.parquet")
    df.to_parquet(path)
    return path

# @task(name="write GCS",log_prints=True)
# def write_gcs(path: Path) -> None:
#     """Write local parquet file to GCS"""
#     gcp_cloud_storage_bucket_block = GcsBucket.load("de-zoomcamp-gcs")
#     gcp_cloud_storage_bucket_block.upload_from_path(
#         from_path=f"{path}",
#         to_path=path
#     )
#     return

@flow(name="ETL Web to GCS")
def etl_web_to_gcs() -> None:
    """Main ETL Function"""
    # assign today's date to variable today via os.system
    # today = dt.date.today().strftime('%Y-%m-%d')
    today = pd.to_datetime('today').date()
    dataset_file = f"{today}_berlin-bike-theft.csv"
    print(dataset_file)
    dataset_url = "https://www.internetwache-polizei-berlin.de/vdb/Fahrraddiebstahl.csv"

    # TODO if file downloaded today exists, skip download
    df_raw = fetch(dataset_url)
    df_clean = clean(df_raw)
    path = write_local(df_clean, dataset_file)
    # write_gcs(path)

if __name__ == "__main__":
    etl_web_to_gcs()