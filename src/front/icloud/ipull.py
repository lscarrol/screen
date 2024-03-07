import time
from pyicloud import PyiCloudService
from dotenv import load_dotenv
import os
from google.cloud import vision
import openai

# Load keys for APIs
load_dotenv()
apple_id = os.getenv("APPLE_ID")
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


down_screen(apple_id, password)
