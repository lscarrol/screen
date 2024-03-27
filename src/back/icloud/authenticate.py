import os
import json
from pyicloud import PyiCloudService

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

# Usage example
username = ""
password = ""
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