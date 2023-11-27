from pyicloud import PyiCloudService


api = PyiCloudService('lcarroll9208@bths.edu')


for photo in api.photos.albums['Screenshots']:
    download = photo.download()
    with open(photo.filename, 'wb') as opened_file:
        opened_file.write(download.raw.read())