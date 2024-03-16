import os
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify
from pyicloud import PyiCloudService

cred = credentials.Certificate('screenr-cd3f7-firebase-adminsdk-bi4cr-9737ee940f.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    try:
        api = PyiCloudService(username, password)
        requires_2fa = api.requires_2fa

        if requires_2fa:
            # Store the authenticated PyiCloudService object in Firestore
            doc_ref = db.collection('sessions').document(username)
            doc_ref.set({'api': api})
            return jsonify({'requires2FA': True})
        else:
            # Login successful, perform any necessary actions
            return jsonify({'success': True})

    except Exception as e:
        return jsonify({'error': str(e)}), 401

@app.route('/api/validate-2fa', methods=['POST'])
def validate_2fa():
    data = request.json
    username = data['username']
    two_factor_code = data['twoFactorCode']

    try:
        # Retrieve the authenticated PyiCloudService object from Firestore
        doc_ref = db.collection('sessions').document(username)
        doc = doc_ref.get()
        api = doc.to_dict()['api']

        if api.validate_2fa_code(two_factor_code):
            # 2FA validation successful
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Invalid 2FA code'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/trigger-scheduled-function', methods=['POST'])
def trigger_scheduled_function():
    data = request.json
    username = data['username']

    try:
        # Retrieve the authenticated PyiCloudService object from Firestore
        doc_ref = db.collection('sessions').document(username)
        doc = doc_ref.get()
        api = doc.to_dict()['api']

        # Pass the authenticated API object to the scheduled function
        from scheduled_function import process_screenshots
        process_screenshots(api)

        return jsonify({'success': True})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/categorized-data', methods=['GET'])
def get_categorized_data():
    try:
        categorized_data = []
        docs = db.collection('categorized_data').get()
        for doc in docs:
            data = doc.to_dict()
            categorized_data.append(data)
        return jsonify(categorized_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)