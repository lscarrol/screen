import os
import tempfile

from google.cloud import storage, vision

storage_client = storage.Client()
client = vision.ImageAnnotatorClient()
image = vision.Image()


def detect_text(data):
    """ Detect text in image

    Args:
        data: Pub/Sub message data
    """
    file_data = data

    file_name = file_data["name"]
    bucket_name = file_data["bucket"]
    source_bucket = storage_client.get_bucket(bucket_name)
    print(f"Analyzing {file_name}.")
    blob = storage_client.bucket(bucket_name).get_blob(file_name)
    blob_uri = f"gs://{bucket_name}/{file_name}"
    image.source.image_uri = blob_uri
    response = client.text_detection(image=image)
    texts = response.text_annotations

    retstr = ""
    for text in texts:
        retstr = retstr + text.description + " "
    

    print(retstr)


    return retstr