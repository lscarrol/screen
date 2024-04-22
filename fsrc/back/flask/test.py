import unittest
from unittest.mock import patch
from app import call_gpt3, detect_text, down_screen

class TestCallGpt3(unittest.TestCase):
    @patch('app.openai.completions.create')
    def test_call_gpt3(self, mock_create):
        # Mock the response from GPT-3
        mock_create.return_value.choices = [{'text': 'Mocked GPT-3 response'}]
        
        # Call the function with a sample request
        response = call_gpt3("Sample request", None)
        
        # Assert that the mocked response is returned
        self.assertEqual(response, 'Mocked GPT-3 response')
        
        # Assert that the mock was called with the correct arguments
        mock_create.assert_called_once_with(
            model="gpt-3.5-turbo-instruct",
            prompt="What do you think this text is: Sample request Return the result in this format: Category | Name | Location (if applicable) | Short Description",
            max_tokens=60
        )


class TestDetectText(unittest.TestCase):
    @patch('app.vision.ImageAnnotatorClient')
    def test_detect_text(self, mock_client):
        # Mock the response from Google Cloud Vision
        mock_client.return_value.text_detection.return_value.text_annotations = [{'description': 'Mocked detected text'}]
        
        # Call the function with a sample image path
        detected_text = detect_text("path/to/image.jpg")
        
        # Assert that the mocked text is returned
        self.assertEqual(detected_text, 'Mocked detected text')
