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
import os
from dotenv import load_dotenv
import threading


auth_json_content = os.environ['AUTH_JSON']
auth_json = json.loads(auth_json_content)
cred = credentials.Certificate(auth_json)
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "https://screen-dm0qgdggc-lscarrols-projects.vercel.app", "methods": ["GET", "POST"]}})

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]


def run_down_screen(api, username):
    thread = threading.Thread(target=down_screen, args=(api, username))
    thread.start()

def call_gpt3(request, categories):
    openai.api_key = os.environ["OPENAI_API_KEY"]

    prompt = f"What do you think this text is: {request}\n\n"
    prompt += "Return the result in this format:\n"
    prompt += "Category | Name | Location (if applicable) | Short Description\n"
    prompt += "If any of the fields are not applicable or cannot be determined, use 'N/A' as the value.\n"
    prompt += "Always return the result in the specified format with 4 fields separated by '|'."

    response = openai.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=1000
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

def down_screen(api, username):
    while True:
        # Get the list of photos
        photos = api.photos.albums['Screenshots']
        
        # Iterate through each photo in the album
        for photo in photos:
            # Check if the screenshot has been processed before
            screenshot_ref = db.collection('screenshots').document(username).collection('screenshots').document(photo.filename)
            screenshot_doc = screenshot_ref.get()
            
            if not screenshot_doc.exists:
                # Download the screenshot
                download = photo.download()
                
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

                    

                    if len(gpt3_response.split('|')) != 4:
                        print("GPT-3 response does not match the expected format.")
                        category, name, location, description = 'N/A', 'N/A', 'N/A', 'N/A'
                        screenshot_ref.set({
                        'filename': photo.filename,
                        'detected_text': detected_text,
                        'timestamp': firestore.SERVER_TIMESTAMP
                        })
                        continue

                    else:
                        category, name, location, description = gpt3_response.split('|')
                        category = category.strip()
                        name = name.strip()
                        location = location.strip()
                        description = description.strip()
                    
                    # Save the screenshot details and extracted data in Firestore
                    if name and '/' not in name:
                        category_ref = db.collection('screenshots').document(username).collection('categories').document(name)
                        category_ref.set({
                            'category': category,
                            'location': location,
                            'description': description
                        })
                    else:
                        name = name.replace('/', '-')
                        print("Invalid name for category document.")
                    screenshot_ref.set({
                        'filename': photo.filename,
                        'detected_text': detected_text,
                        'timestamp': firestore.SERVER_TIMESTAMP
                    })
                # Delete the temporary file
                os.unlink(temp_file_path)
            else:
                # If the screenshot has already been processed, break the loop
                break
        
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

    run_down_screen(api, username)
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
            run_down_screen(api, username)
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

