import os
from google.cloud import storage

def upload_files_to_bucket(bucket_name, source_folder):
   """Uploads all files in a folder to a GCP bucket."""
   storage_client = storage.Client()
   bucket = storage_client.bucket(bucket_name)

   # Get all files in the source folder
   files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]

   # Upload each file to the bucket
   for file in files:
       blob = bucket.blob(file)
       blob.upload_from_filename(os.path.join(source_folder, file))
       print(f"File {file} uploaded to {bucket_name}.")

# Use the function
upload_files_to_bucket('screenshots-liam', '../imgs')