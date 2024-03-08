import os
import time
from pyicloud import PyiCloudService
from google.cloud import vision
import openai
import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_functions import https_fn, options, scheduler

# Fetch the service account key JSON file contents
cred = credentials.Certificate('../keys/screen-7b77b-firebase-adminsdk-sdkvq-96747a79e0.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'projectId': 'screen-7b77b',
})

# Get a reference to the Firestore database
db = firestore.client()

# Load environment variables
apple_id = os.environ.get("APPLE_ID")
password = os.environ.get("PASSWORD")
openai.api_key = os.environ.get("OPENAI_API_KEY")

def call_gpt3(request, categories):
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

def detect_text(image_path):
    client = vision.ImageAnnotatorClient()
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    if len(texts) > 0:
        return texts[0].description
    else:
        return None

@scheduler(schedule="every 30 seconds", memory=128)
def down_screen(event):
    try:
        api = PyiCloudService(apple_id, password)

        if api.requires_2fa:
            print("Two-factor authentication required.")
            # Handle 2FA code input or exit the function
            return

        if not api.is_trusted_session:
            print("Session is not trusted. Requesting trust...")
            result = api.trust_session()
            print("Session trust result %s" % result)
            if not result:
                print("Failed to request trust. You will likely be prompted for the code again in the coming weeks")
                return

        # Ensure the screenshots folder exists
        screenshots_folder = os.path.expanduser('screenshots')
        if not os.path.exists(screenshots_folder):
            os.makedirs(screenshots_folder)

        # Get the list of photos
        photos = api.photos.albums['Screenshots']

        # Find the latest screenshot
        photo = next(iter(photos), None)
        if photo is None:
            print("No screenshots found.")
            return

        download = photo.download()
        screenshot_path = f'screenshots/{photo.filename}'
        with open(screenshot_path, 'wb') as opened_file:
            opened_file.write(download.raw.read())
            print(f'Downloaded: {photo.filename}')

        # Check if the screenshot has already been processed
        query = db.collection('processed_screenshots').where('filename', '==', photo.filename).get()
        if query:
            print(f"Screenshot {photo.filename} has already been processed.")
            return

        # Detect text in the downloaded screenshot
        detected_text = detect_text(screenshot_path)
        if detected_text:
            print(f'Detected text: {detected_text}')
            call_gpt3(detected_text, None)

        # Mark the screenshot as processed
        db.collection('processed_screenshots').add({'filename': photo.filename})

    except Exception as e:
        print(f"Error: {str(e)}")