# [START cloudrun_imageproc_handler_analyze]
def detect_text_in_images(data):
  """Detects text in uploaded images and moves them to another bucket.

  Args:
      data: Pub/Sub message data
  """
  file_data = data

  file_name = file_data["name"]
  bucket_name = file_data["bucket"]

  blob = storage_client.bucket(bucket_name).get_blob(file_name)
  blob_uri = f"gs://{bucket_name}/{file_name}"
  blob_source = vision.Image(source=vision.ImageSource(image_uri=blob_uri))

  print(f"Analyzing {file_name}.")

  # Detect text in the image
  result = vision_client.text_detection(image=blob_source)
  detected_texts = result.text_annotations

  # Process detected text
  for text in detected_texts:
      print(f"Detected text: {text.description}")

  # Move the image to another bucket after processing
  new_bucket_name = "imgarchive"
  new_bucket = storage_client.bucket(new_bucket_name)
  new_blob = new_bucket.copy_blob(blob, new_bucket, file_name)
  blob.delete()

  print(f"Image {file_name} moved to: gs://{new_bucket_name}/{file_name}")
# [END cloudrun_imageproc_handler_analyze]
