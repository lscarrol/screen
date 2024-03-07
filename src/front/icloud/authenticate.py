from dotenv import load_dotenv
import os
import sys
import time
from pyicloud import PyiCloudService

load_dotenv()
apple_id = os.getenv("APPLE_ID")
password = os.getenv("PASSWORD")

def down_screen(account, password):
    api = PyiCloudService(account, password)

    if api.requires_2fa:
        print("Two-factor authentication required.")
        code = input("Enter the code you received of one of your approved devices: ")
        result = api.validate_2fa_code(code)
        print("Code validation result: %s" % result)

        if not result:
            print("Failed to verify security code")
            sys.exit(1)

        if not api.is_trusted_session:
            print("Session is not trusted. Requesting trust...")
            result = api.trust_session()
            print("Session trust result %s" % result)

            if not result:
                print("Failed to request trust. You will likely be prompted for the code again in the coming weeks")

    # Ensure the screenshots folder exists
    screenshots_folder = os.path.expanduser('screenshots')
    if not os.path.exists(screenshots_folder):
        os.makedirs(screenshots_folder)

    # Initialize the last downloaded screenshot timestamp
    last_downloaded_timestamp = None
    latest_screenshot = None
    while True:
        # Get the list of photos
        photos = api.photos.albums['Screenshots']

        # Find the latest screenshot
        photo = next(iter(api.photos.albums['Screenshots']), None)
        download = photo.download()
        if ((latest_screenshot == None) or latest_screenshot != photo.filename):
            with open('screenshots/' + photo.filename, 'wb') as opened_file:
                opened_file.write(download.raw.read())
            print(f'Downloaded: {photo.filename}')
            latest_screenshot = photo.filename
        

        # Wait for a while before checking again
        # Adjust the sleep time as needed
        time.sleep(10) # Check every 5 seconds

down_screen(apple_id, password)
