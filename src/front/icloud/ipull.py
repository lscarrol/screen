import time
from pyicloud import PyiCloudService
from dotenv import load_dotenv
import os

# Load key for api
load_dotenv()
icloud = os.getenv("ICLOUD")
password = os.getenv("PASSWORD")

def down_screen(account, password):
  api = PyiCloudService(account, password)

  last_photo_date = None

  while True:
      for photo in api.photos.albums['Screenshots']:
          # Skip photos that were already downloaded
          if last_photo_date and photo.asset_date <= last_photo_date:
              continue

          download = photo.download()
          with open(photo.filename, 'wb') as opened_file:
              opened_file.write(download.raw.read())

          # Update the date of the last downloaded photo
          last_photo_date = photo.asset_date

      # Wait for a short period before checking again
      time.sleep(1)

# Replace 'your_apple_id' with your actual Apple ID
down_screen(icloud, password)
