from pyicloud import PyiCloudService


def down_screen(account):
    api = PyiCloudService(account)
    for photo in api.photos.albums['Screenshots']:
        download = photo.download()
        with open(photo.filename, 'wb') as opened_file:
            opened_file.write(download.raw.read())