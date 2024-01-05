from pyicloud import PyiCloudService

api = PyiCloudService()
if not api.authenticate(store_in_keyring=True):
  print("Failed to authenticate")
else:
  print("Authenticated successfully")