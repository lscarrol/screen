import os
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_functions import https_fn
from flask_cors import CORS
from pyicloud import PyiCloudService
import json

cred = credentials.Certificate('auth.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def initialize_api(username, password, session_data=None):
    if session_data:
        api = PyiCloudService(apple_id=username, password="")
        api.session_data = session_data
        api.authenticate()
    else:
        api = PyiCloudService(apple_id=username, password=password)
    return api

@https_fn.on_request()
def login(request: https_fn.Request) -> https_fn.Response:
    data = request.get_json()
    username = data['username']
    password = data['password']

    try:
        # Check if session data exists in Firestore
        session_doc = db.collection('sessions').document(username).get()
        if session_doc.exists:
            session_data = session_doc.to_dict()
            api = initialize_api(username, "", session_data=session_data)
        else:
            api = initialize_api(username, password)

        if api.requires_2fa:
            devices = api.trusted_devices
            return https_fn.Response(json.dumps({'requires2FA': True, 'devices': devices}), content_type='application/json')
        else:
            # Login successful
            from schedule_function import process_screenshots
            process_screenshots(api)
            # Store the session data in Firestore
            db.collection('sessions').document(username).set(api.session_data)
            return https_fn.Response(json.dumps({'success': True}), content_type='application/json')

    except Exception as e:
        return https_fn.Response(json.dumps({'error': str(e)}), content_type='application/json', status=401)


@https_fn.on_request()
def validate_2fa(request: https_fn.Request) -> https_fn.Response:
    data = request.get_json()
    username = data['username']
    password = data['password']
    two_factor_code = data.get('twoFactorCode')

    try:
        # Check if session data exists in Firestore
        session_doc = db.collection('sessions').document(username).get()
        if session_doc.exists:
            session_data = session_doc.to_dict()
            api = initialize_api(username, "")
        else:
            api = initialize_api(username, password)

        if api.requires_2fa:
            if two_factor_code:
                # Validate the 2FA code
                result = api.validate_2fa_code(two_factor_code)
                if result:
                    # 2FA validation successful
                    from schedule_function import process_screenshots
                    process_screenshots(api)
                    # Store the session data in Firestore
                    db.collection('sessions').document(username).set(api.session_data)
                    return https_fn.Response(json.dumps({'success': True}), content_type='application/json')
                else:
                    return https_fn.Response(json.dumps({'error': 'Invalid 2FA code'}), content_type='application/json', status=401)
        else:
            # Login successful
            from schedule_function import process_screenshots
            process_screenshots(api)
            # Store the session data in Firestore
            db.collection('sessions').document(username).set(api.session_data)
            return https_fn.Response(json.dumps({'success': True}), content_type='application/json')

    except Exception as e:
        return https_fn.Response(json.dumps({'error': str(e)}), content_type='application/json', status=401)


@https_fn.on_request()
def check_login(request: https_fn.Request) -> https_fn.Response:
    # Get the username from the session cookie or request data
    username = request.cookies.get('username') or request.get_json().get('username')
    if username:
        # Check if session data exists in Firestore
        session_doc = db.collection('sessions').document(username).get()
        if session_doc.exists:
            return https_fn.Response(json.dumps({'loggedIn': True}), content_type='application/json')

    return https_fn.Response(json.dumps({'loggedIn': False}), content_type='application/json')

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