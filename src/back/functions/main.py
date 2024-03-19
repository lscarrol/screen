import os
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_functions import https_fn
from flask_cors import CORS
from pyicloud import PyiCloudService
import json

cred = credentials.Certificate('screenr-cd3f7-firebase-adminsdk-bi4cr-9737ee940f.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

@https_fn.on_request()
def login(request: https_fn.Request) -> https_fn.Response:
    data = request.get_json()
    username = data['username']
    password = data['password']

    try:
        api = PyiCloudService(username, password)

        if api.requires_2fa:
            devices = api.trusted_devices
            client_id = api.client_id
            print(client_id)
            doc_ref = db.collection('sessions').document(username)
            doc_ref.set({'client_id': client_id})
            # Return the list of trusted devices to the client
            return https_fn.Response(json.dumps({'requires2FA': True, 'devices': devices}), content_type='application/json')
        else:
            # Login successful, store the client_id in Firestore
            client_id = api.client_id
            doc_ref = db.collection('sessions').document(username)
            doc_ref.set({'client_id': client_id})
            return https_fn.Response(json.dumps({'success': True}), content_type='application/json')
    except Exception as e:
        return https_fn.Response(json.dumps({'error': str(e)}), content_type='application/json', status=401)

@https_fn.on_request()
def validate_2fa(request: https_fn.Request) -> https_fn.Response:
    try:
        # Log the request data
        print('Request data:', request.data)

        data = request.get_json()
        username = data['username']
        two_factor_code = data['twoFactorCode']

        # Retrieve the client_id from Firestore
        doc_ref = db.collection('sessions').document(username)
        doc = doc_ref.get()
        client_id = doc.to_dict()['client_id']

        # Create a new PyiCloudService instance using the client_id
        api = PyiCloudService(username, client_id=client_id)

        result = api.validate_2fa_code(two_factor_code)

        if result:
            # 2FA validation successful
            return https_fn.Response(json.dumps({'success': True}), content_type='application/json')
        else:
            return https_fn.Response(json.dumps({'error': 'Invalid 2FA code'}), content_type='application/json', status=401)

    except json.JSONDecodeError as e:
        # Log the JSON parsing error
        print('JSON Parsing Error:', str(e))
        return https_fn.Response(json.dumps({'error': 'Invalid JSON data'}), content_type='application/json', status=400)

    except Exception as e:
        # Log the error and the response data
        print('2FA Validation Error:', str(e))
        print('Response data:', request.data)
        return https_fn.Response(json.dumps({'error': str(e)}), content_type='application/json', status=500)
        
@https_fn.on_request()
def trigger_scheduled_function(request: https_fn.Request) -> https_fn.Response:
    data = request.get_json()
    username = data['username']
    password = data['password']  # Add this line to receive the password from the request

    try:
        # Create a new PyiCloudService instance using the provided username and password
        api = PyiCloudService(username, password)

        # Pass the authenticated API object to the scheduled function
        from scheduled_function import process_screenshots
        process_screenshots(api)

        return https_fn.Response(json.dumps({'success': True}), content_type='application/json')
    except Exception as e:
        return https_fn.Response(json.dumps({'error': str(e)}), content_type='application/json', status=500)

@https_fn.on_request()
def get_categorized_data(request: https_fn.Request) -> https_fn.Response:
    try:
        categorized_data = []
        docs = db.collection('categorized_data').get()
        for doc in docs:
            data = doc.to_dict()
            categorized_data.append(data)
        return https_fn.Response(json.dumps(categorized_data), content_type='application/json')
    except Exception as e:
        return https_fn.Response(json.dumps({'error': str(e)}), content_type='application/json', status=500)