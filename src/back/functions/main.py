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
    print(username)
    print(password)
    try:
        api = PyiCloudService(username, password)
        
        if api.requires_2fa:
            # Store the authenticated PyiCloudService object in Firestore
            doc_ref = db.collection('sessions').document(username)
            doc_ref.set({'api': api})
            return https_fn.Response(json.dumps({'requires2FA': True}), content_type='application/json')
        else:
            # Login successful, perform any necessary actions
            return https_fn.Response(json.dumps({'success': True}), content_type='application/json')
    except Exception as e:
        return https_fn.Response(json.dumps({'error': str(e)}), content_type='application/json', status=401)

@https_fn.on_request()
def validate_2fa(request: https_fn.Request) -> https_fn.Response:
    data = request.get_json()
    username = data['username']
    two_factor_code = data['twoFactorCode']
    
    try:
        # Retrieve the authenticated PyiCloudService object from Firestore
        doc_ref = db.collection('sessions').document(username)
        doc = doc_ref.get()
        api = doc.to_dict()['api']
        
        result = api.validate_2fa_code(two_factor_code)
        
        if result:
            # 2FA validation successful
            return https_fn.Response(json.dumps({'success': True}), content_type='application/json')
        else:
            return https_fn.Response(json.dumps({'error': 'Invalid 2FA code'}), content_type='application/json', status_code=401)
    except Exception as e:
        return https_fn.Response(json.dumps({'error': str(e)}), content_type='application/json', status=500)

@https_fn.on_request()
def trigger_scheduled_function(request: https_fn.Request) -> https_fn.Response:
    data = request.get_json()
    username = data['username']
    
    try:
        # Retrieve the authenticated PyiCloudService object from Firestore
        doc_ref = db.collection('sessions').document(username)
        doc = doc_ref.get()
        api = doc.to_dict()['api']
        
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