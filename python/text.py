# Import Packages
import os
from google.cloud import storage
import pandas as pd

# Environment Variable
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'E:\\GCP\\hackstaticboss\\Service Account Key\\hackathon-springml-2019.json'

# GCS Bucket Properties
bucket_name = 'speech-to-text-hackathon'
source_blob_name = 'result/2019/part-m-00000'
destination_file_name = 'E:\\text.csv'
blob_name = 'result/2019'

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


# This function deletes the folder where the text data is stored.
def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blobs = bucket.list_blobs(prefix='result/2019')
    for blob in blobs:
        blob.delete()

    print('Blob {} deleted.'.format(blob_name))


# CSV to Text Function
def csv_to_text(csv_file):
    df = pd.read_csv(csv_file)
    text = df.columns[1]
    print(text)


# Function Call
download_file(bucket_name, source_blob_name, destination_file_name)
delete_blob(bucket_name, blob_name)
csv_to_text(csv_file)
