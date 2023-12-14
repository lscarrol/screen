import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from google.cloud import storage
from pyicloud import PyiCloudService
from pymongo import MongoClient

def upload_files_to_bucket(bucket_name, source_folder):
  """Uploads all files in a folder to a GCP bucket."""
  storage_client = storage.Client()
  bucket = storage_client.bucket(bucket_name)

  # Get all files in the source folder
  files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]

  # Upload each file to the bucket
  for file in files:
      # Check if the file is a duplicate
      client = MongoClient('mongodb://localhost:27017/')
      db = client['screenshot_db']
      collection = db['screenshots']
      if collection.count_documents({"filename": file}) == 0:
          blob = bucket.blob(file)
          blob.upload_from_filename(os.path.join(source_folder, file))
          print(f"File {file} uploaded to {bucket_name}.")
          collection.insert_one({"filename": file})

def down_screen(account):
   api = PyiCloudService(account)
   for photo in api.photos.albums['Screenshots']:
       download = photo.download()
       with open(photo.filename, 'wb') as opened_file:
           opened_file.write(download.raw.read())

class Handler(FileSystemEventHandler):
  def on_created(self, event):
      if event.is_directory:
          return None
      else:
          # Call the function to upload the file to the GCP bucket
          upload_files_to_bucket('your-bucket-name', event.src_path)

def run_daemon(path):
  event_handler = Handler()
  observer = Observer()
  observer.schedule(event_handler, path, recursive=False)
  observer.start()

  try:
      while True:
          time.sleep(1)
  except KeyboardInterrupt:
      observer.stop()

  observer.join()

if __name__ == '__main__':
  run_daemon('/path/to/watch')