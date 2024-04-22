from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
import tempfile
from pyicloud import PyiCloudService
import json
import time
from dotenv import load_dotenv
from google.cloud import vision
import openai

cred = credentials.Certificate('auth.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)
CORS(app)


def call_gpt3(request, categories):
    openai.api_key = os.getenv('OPENAI_API_KEY')

    response = openai.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt="What do you think this text is: " + \
        request + \
        " Return the result in this format: Category | Name | Location (if applicable) | Short Description",
        max_tokens=100
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
    while True:
        # Get the list of photos
        photos = api.photos.albums['Screenshots']

        # Find the latest screenshot
        photo = next(iter(api.photos.albums['Screenshots']), None)
        download = photo.download()

        # Check if the screenshot has been processed before
        screenshot_ref = db.collection('screenshots').document(photo.filename)
        screenshot_doc = screenshot_ref.get()

        if not screenshot_doc.exists:
            # Save the screenshot to a temporary file
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(download.raw.read())
                temp_file_path = temp_file.name

            print(f'Downloaded: {photo.filename}')

            # Detect text in the downloaded screenshot
            detected_text = detect_text(temp_file_path)

            if detected_text:
                print(f'Detected text: {detected_text}')

                # Pass the detected text to GPT-3
                gpt3_response = call_gpt3(detected_text, None)
                print(f'GPT-3 response: {gpt3_response}')

                # Save the screenshot details and GPT-3 response in Firestore
                screenshot_ref.set({
                    'filename': photo.filename,
                    'detected_text': detected_text,
                    'gpt3_response': gpt3_response,
                    'timestamp': firestore.SERVER_TIMESTAMP
                })

            # Delete the temporary file
            os.unlink(temp_file_path)

        # Wait for a while before checking again
        # Adjust the sleep time as needed
        time.sleep(10)  # Check every 10 seconds

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    api = PyiCloudService(username, password)

    if api.requires_2fa:
        return jsonify({'requires_2fa': True})

    down_screen(api)
    session_data = api.session_data
    db.collection('sessions').document(username).set(session_data)

    return jsonify({'success': True})

@app.route('/api/login_with_session', methods=['POST'])
def login_with_session():
    data = request.get_json()
    username = data['username']

    session_doc = db.collection('sessions').document(username).get()

    if session_doc.exists:
        session_data = session_doc.to_dict()
        api = PyiCloudService(username, "")
        api.session_data = session_data
        api.session.cookies.load(ignore_discard=True, ignore_expires=True)

        try:
            api.authenticate()
            down_screen(api)
            return jsonify({'success': True})
        except:
            return jsonify({'success': False, 'message': 'Failed to authenticate with saved session.'})
    else:
        return jsonify({'success': False, 'message': 'Session not found.'})

@app.route('/api/validate_2fa', methods=['POST'])
def validate_2fa():
    data = request.get_json()
    username = data['username']
    password = data['password']
    code = data['code']

    api = PyiCloudService(username, password)
    result = api.validate_2fa_code(code)

    if result:
        session_data = api.session_data
        db.collection('sessions').document(username).set(session_data)
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Failed to verify 2FA code.'})

if __name__ == '__main__':
    app.run()