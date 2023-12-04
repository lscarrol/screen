from google.cloud import storage

def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    blobs = bucket.list_blobs()
    arr = []
    for blob in blobs:
        arr.append(f"gs://{bucket_name}/{blob.name}")
    return arr