import os
from os.path import join, dirname
from dotenv import main
import boto3

class Storage:
    s3 = None

    def __init__(self):
        dotenv_path = join(dirname(__file__), '.env')
        main.load_dotenv(dotenv_path)

        self.s3 = boto3.client('s3', aws_access_key_id = str(os.environ.get("AWS_ACCESS_KEY_ID")),
                                aws_secret_access_key = str(os.environ.get("AWS_SECRET_ACCESS_KEY")),
                                aws_session_token = str(os.environ.get("AWS_SESSION_TOKEN")))

    def create_bucket(self, bucket_name: str):
        try:
            return self.s3.create_bucket(Bucket=bucket_name)
        except Exception as err:
            print(err)
            return

    def upload_file(self, file, bucket_name, object_name):
        try:
        #     self.s3.upload_file(file, bucket_name, object_name)
        #     os.remove(path=file)
            self.s3.put_object(Body=file, Bucket=bucket_name, Key=object_name)
        except Exception as err:
            print(err)
            return

    def bucket_exists(self, bucket_name):
        try:
            if self.s3.head_bucket(Bucket=bucket_name):
                return True
            else: return False
        except Exception as err:
            print(err)
            return False