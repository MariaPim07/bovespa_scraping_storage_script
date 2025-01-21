from io import BytesIO
from datetime import datetime
from s3_storage import Storage
from bovespa_scrapper_data import BovespaScrapperData
import pandas as pd

storage = Storage()
bovespaScrapperData = BovespaScrapperData()

def main():
    try:
        bucket_name: str = "script-raw-data-bovespa"
        today = datetime.now()

        if not storage.bucket_exists(bucket_name):
            storage.create_bucket(bucket_name)

        data = bovespaScrapperData.find_data()

        df = pd.DataFrame([d.__dict__ for d in data])

        file = pd.DataFrame([d.__dict__ for d in data]).to_parquet()

        object_name = f"{today.year}/{today.month}/{today.day}/bovespa.parquet"

        storage.upload_file(file, bucket_name, object_name)
    except Exception as error:
        print(error)


if __name__ == "__main__":
    main()