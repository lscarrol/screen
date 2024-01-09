import time
from pyicloud import PyiCloudService
from dotenv import load_dotenv
import os
from google.cloud import vision
import openai

# Load keys for APIs
load_dotenv()
icloud = os.getenv("ICLOUD")
password = os.getenv("PASSWORD")
openai.api_key = os.getenv("OPENAI_API_KEY")

def call_gpt3(request, categories):
    openai.api_key = os.getenv('OPENAI_API_KEY')

    response = openai.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt="What do you think this text is: " + request,
        max_tokens=60
    )

    return response.choices[0].text.strip()


def down_screen(account, password):
    api = PyiCloudService(account, password)

    last_photo_date = None

    # Initialize the Vision client
    client = vision.ImageAnnotatorClient()
    direct = 'imgs/'
    while True:
        for photo in api.photos.albums['Screenshots']:
            # Skip photos that were already downloaded
               
            if last_photo_date and photo.asset_date <= last_photo_date:
                continue
            
            download = photo.download()
            with open(direct + photo.filename, 'wb') as opened_file:
                opened_file.write(download.raw.read())

            # Use the Vision API to detect text in the image
            with open(direct + photo.filename, 'rb') as image_file:
                content = image_file.read()
            image = vision.Image(content=content)
            response = client.text_detection(image=image)
            # print(response)
            texts = response.text_annotations

            if len(texts) > 0:
                text = texts[0].description
                print(text)
                print(call_gpt3(text))
            # Update the date of the last downloaded photo
            last_photo_date = photo.asset_date
        # Wait for a short period before checking again
        time.sleep(1)

# Replace 'your_apple_id' with your actual Apple ID
down_screen(icloud, password)
