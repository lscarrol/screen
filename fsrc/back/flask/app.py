import time
from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
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

app = Flask(__name__)
socketio = SocketIO(app)

def call_gpt3(request, categories):
    response = openai.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt="What do you think this text is: " + \
        request + \
        " Return the result in this format: Category | Name | Location (if applicable) | Short Description",
        max_tokens=60
    )
    return response.choices[0].text.strip()

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

def down_screen(account, password):
    api = PyiCloudService(account, password)
    if api.requires_2fa:
        print("Two-factor authentication required.")
        code = input("Enter the code you received of one of your approved devices: ")
        result = api.validate_2fa_code(code)
        print("Code validation result: %s" % result)
        if not result:
            print("Failed to verify security code")
            return
        if not api.is_trusted_session:
            print("Session is not trusted. Requesting trust...")
            result = api.trust_session()
            print("Session trust result %s" % result)
            if not result:
                print("Failed to request trust. You will likely be prompted for the code again in the coming weeks")
                return
    screenshots_folder = os.path.expanduser('screenshots')
    if not os.path.exists(screenshots_folder):
        os.makedirs(screenshots_folder)
    last_downloaded_timestamp = None
    latest_screenshot = None
    while True:
        photos = api.photos.albums['Screenshots']
        photo = next(iter(api.photos.albums['Screenshots']), None)
        download = photo.download()
        if ((latest_screenshot == None) or latest_screenshot != photo.filename):
            with open('screenshots/' + photo.filename, 'wb') as opened_file:
                opened_file.write(download.raw.read())
            print(f'Downloaded: {photo.filename}')
            latest_screenshot = photo.filename
            detected_text = detect_text('screenshots/' + photo.filename)
            if detected_text:
                # print(f'Detected text: {detected_text}')
                gpt3_response = call_gpt3(detected_text, None)
                print(f'GPT-3 response: {gpt3_response}')
                
                emit('gpt3_update', {'message': gpt3_response}, broadcast=True)
        time.sleep(10) # Check every 5 seconds

# Start the continuous updates process automatically when the application is launched
socketio.start_background_task(down_screen, apple_id, password)

@app.route('/start_continuous_updates', methods=['POST'])
def start_continuous_updates():
    
    return jsonify({"message": "Continuous updates started"})

if __name__ == '__main__':
    socketio.run(app, debug=True)
