from google.cloud import storage, vision
from transformers import pipeline
import signal

def list_blobs(bucket_name):
   """Lists all the blobs in the bucket."""
   storage_client = storage.Client()
   bucket = storage_client.get_bucket(bucket_name)
   blobs = list(bucket.list_blobs())
   print(f"Found {len(blobs)} blobs in bucket {bucket_name}")
   return blobs

def detect_text_uri(uri, timeout=5):
   """Detects text in the file located in Google Cloud Storage or on the Web."""
   client = vision.ImageAnnotatorClient()
   image = vision.Image()
   image.source.image_uri = uri

   # Set up a signal handler to raise an exception if the function takes too long1
   def handler(signum, frame):
       raise TimeoutError("Timeout")
   signal.signal(signal.SIGALRM, handler)
   signal.alarm(timeout)

   try:
       response = client.text_detection(image=image)
   except TimeoutError:
       print(f"Timeout while processing {uri}")
       return None
   finally:
       signal.alarm(0) # Disable the alarm

   texts = response.text_annotations
   if texts:
       print(f"Detected text in {uri}: {texts[0].description}")
   else:
       print(f"No text detected in {uri}")
   return texts[0].description if texts else None

def process_images(bucket_name, batch_size=10):
   """Processes all images in a GCS bucket."""
   blobs = list_blobs(bucket_name)
   for i in range(0, len(blobs), batch_size):
       batch = blobs[i:i+batch_size]
       for blob in batch:
           text = detect_text_uri(blob.public_url)
           if text:
               print(f"Text extracted from {blob.name}: {text}")
               categorized_text = generate_text(text)
               print(f"Categorized text: {categorized_text}")

process_images('screenshots-liam')
