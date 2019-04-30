# Import Packages
import os
from google.cloud import storage
import pandas as pd

# Environment Variable
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'E:\\GCP\\hackstaticboss\\Service Account Key\\hackathon-springml-2019.json'

# GCS Bucket Properties
bucket_name = 'speech-to-text-hackathon'
source_blob_name = 'result/16/part-m-00000'
destination_file_name = 'E:\\text.csv'

# Local Downloaded CSV File Properties
csv_file = 'E:\\text.csv'

def download_file(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

    print('Blob {} downloaded to {}.'.format(
        source_blob_name,
        destination_file_name))


def csv_to_text(csv_file):
    df = pd.read_csv(csv_file)
    text = df.columns[1]
    print(text)


download_file(bucket_name, source_blob_name, destination_file_name)
csv_to_text(csv_file)
