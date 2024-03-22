import os
import time
from google.cloud import vision, storage
import openai
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase

db = firestore.client()

# Initialize Google Cloud Storage client
storage_client = storage.Client()

def process_screenshots(api):
    while True:
        # Get the list of photos
        photos = api.photos.albums['Screenshots']

        # Find the latest screenshot
        photo = next(iter(photos), None)
        if photo is None:
            print("No screenshots found.")
            time.sleep(60)  # Wait for 60 seconds before checking again
            continue

        # Check if the screenshot has already been processed
        query = db.collection('processed_screenshots').where('filename', '==', photo.filename).get()
        if query:
            print(f"Screenshot {photo.filename} has already been processed.")
            time.sleep(60)  # Wait for 60 seconds before checking again
            continue

        # Download the screenshot
        download = photo.download()

        # Upload the screenshot to Google Cloud Storage
        bucket_name = 'screenshot_arch'  # Replace with your actual bucket name
        blob_name = f'screenshots/{photo.filename}'
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_string(download.raw.read(), content_type='image/jpeg')
        print(f'Uploaded: {photo.filename}')

        # Detect text in the uploaded screenshot
        detected_text = detect_text_from_uri(f'gs://{bucket_name}/{blob_name}')
        if detected_text:
            print(f'Detected text: {detected_text}')
            call_gpt3(detected_text, None)

        # Mark the screenshot as processed
        db.collection('processed_screenshots').add({'filename': photo.filename})

        time.sleep(60)  # Wait for 60 seconds before processing the next screenshot

def detect_text_from_uri(uri):
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = uri
    response = client.text_detection(image=image)
    texts = response.text_annotations
    if len(texts) > 0:
        return texts[0].description
    else:
        return None

def call_gpt3(request, categories):
    openai.api_key = "os.getenv("OPENAI_API_KEY")"
    response = openai.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt="What do you think this text is: " + request + " Return the result in this format: Category | Name | Location (if applicable) | Short Description",
        max_tokens=60
    )

    gpt3_response = response.choices[0].text.strip()
    print(f'GPT-3 response: {gpt3_response}')

    # Store the response in Firestore, but check for duplicates first
    category, name, location, description = gpt3_response.split(' | ')
    data = {
        'category': category,
        'name': name,
        'location': location if location else None,
        'description': description
    }

    # Check if a document with the same name already exists
    query = db.collection('categorized_data').where('name', '==', name).get()
    if not query:
        db.collection('categorized_data').add(data)
    else:
        print(f"Duplicate entry: {name}")