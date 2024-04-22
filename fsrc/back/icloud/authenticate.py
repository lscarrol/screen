import os
import json
from pyicloud import PyiCloudService
import time
from dotenv import load_dotenv
from google.cloud import vision
import openai

load_dotenv()
apple_id = os.getenv("APPLE_ID")
password = os.getenv("PASSWORD")
openai.api_key = os.getenv("OPENAI_API_KEY")

def authenticate_with_2fa(username, password, session_directory):
    api = PyiCloudService(username, password)

    if api.requires_2fa:
        print("Two-factor authentication required.")
        code = input("Enter the 2FA code: ")
        result = api.validate_2fa_code(code)
        if not result:
            print("Failed to verify 2FA code")
            return None

    # Save the session data
    session_path = os.path.join(session_directory, f"{username}.session")
    with open(session_path, "w", encoding="utf-8") as session_f:
        json.dump(api.session_data, session_f)

    print("Logged in successfully. Session saved.")
    return api

def authenticate_with_session(username, session_directory):
    session_path = os.path.join(session_directory, f"{username}.session")

    try:
        with open(session_path, encoding="utf-8") as session_f:
            session_data = json.load(session_f)
    except FileNotFoundError:
        print("Session file not found. Please log in with credentials first.")
        return None

    api = PyiCloudService(username, "")
    api.session_data = session_data
    api.session.cookies.load(ignore_discard=True, ignore_expires=True)

    try:
        api.authenticate()
        print("Logged in successfully using saved session.")
        return api
    except:
        print("Failed to authenticate with saved session. Please log in with credentials and 2FA again.")
        return None


def call_gpt3(request, categories):
    openai.api_key = os.getenv('OPENAI_API_KEY')

    response = openai.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt="What do you think this text is: " + \
        request + \
        " Return the result in this format: Category | Name | Location (if applicable) | Short Description",
        max_tokens=60
    )

    return response.choices[0].text.strip()

def detect_text(image_path):
    """Detects text in the file located in Google Cloud Storage or on the Web."""
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

def down_screen(api):
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
        
            # Detect text in the downloaded screenshot
            detected_text = detect_text('screenshots/' + photo.filename)
            if detected_text:
                print(f'Detected text: {detected_text}')
                # Pass the detected text to GPT-3
                gpt3_response = call_gpt3(detected_text, None)
                print(f'GPT-3 response: {gpt3_response}')
        # Wait for a while before checking again
        # Adjust the sleep time as needed
        time.sleep(10) # Check every 5 seconds


# Usage example
username = apple_id
session_directory = "./sessions"

# Create the session directory if it doesn't exist
os.makedirs(session_directory, exist_ok=True)

# Log in with credentials and 2FA
api = authenticate_with_2fa(username, password, session_directory)

if api is None:
    print("Authentication failed.")
    exit(1)

# Perform operations with the authenticated API
# ...

# Log in with saved session
api = authenticate_with_session(username, session_directory)

if api is None:
    print("Authentication failed.")
    exit(1)

# Perform operations with the authenticated API
# ...


down_screen(api)