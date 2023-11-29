# iCloud to GCP Text Extraction and Categorization

## Overview
This project is designed to facilitate the extraction of screenshots from iCloud, uploading them to a Google Cloud Platform (GCP) bucket, extracting text using Google Cloud Vision API, categorizing the extracted text using GPT (Generative Pre-trained Transformer), creating categorized lists, and finally sending them back to a client application. The entire workflow is orchestrated using serverless GCP services including Cloud Functions, Cloud Run, and Pub/Sub.

## Features
- Pulls screenshots from iCloud storage.
- Uploads screenshots to a specified GCP bucket.
- Utilizes Google Cloud Vision API for text extraction from the screenshots.
- Employs GPT for categorizing the extracted text.
- Generates categorized lists from the extracted and categorized text.
- Sends the categorized lists back to a client application.

## Components
1. **iCloud Pull**
   - Fetches screenshots from iCloud storage.

2. **GCP Bucket Upload**
   - Transfers the fetched screenshots to a designated GCP bucket for further processing.

3. **Text Extraction with Cloud Vision**
   - Utilizes Google Cloud Vision API to extract text from the uploaded screenshots.

4. **Categorization with GPT**
   - Uses GPT (Generative Pre-trained Transformer) to categorize the extracted text.

5. **List Creation**
   - Organizes the categorized text into lists based on the identified categories.

6. **Client App Integration**
   - Sends the created lists back to a client application for user access.

## Technologies Used
- **Google Cloud Platform (GCP) Services**:
  - Cloud Functions: Orchestrating the workflow.
  - Cloud Run: Running serverless containers for specific tasks.
  - Pub/Sub: Messaging service for communication between components.
  - Cloud Storage: Storing screenshots in GCP buckets.
  - Cloud Vision API: Extracting text from screenshots.
  - GPT: Categorizing extracted text.

## Usage
- Configure the system to fetch screenshots from iCloud periodically.
- Access the client application to view the categorized lists generated from the extracted text.

## Contributors
- [oswald]

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
