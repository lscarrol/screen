# Screen

## Overview

This project empowers you to effortlessly transform screenshots on your phone into organized, categorized lists. Whether you come across a must-try recipe, a captivating movie recommendation, a trendy restaurant, or a binge-worthy TV show, simply capture a screenshot and your lists will be built automatically. Say goodbye to the hassle of manual organization and hello to a seamless, automated way of keeping track of all the exciting things you discover through your screenshots!

## Features

- Pulls screenshots from iCloud storage.
- Uploads screenshots to a specified Firebase Storage bucket.
- Utilizes Google Cloud Vision API for text extraction from the screenshots.
- Employs GPT for categorizing the extracted text.
- Generates categorized lists from the extracted and categorized text.
- Sends the categorized data to a Firestore database.
- Real-time updates in the frontend application built with Svelte and Tailwind CSS.

## Components

1. **iCloud Pull**
   - Fetches screenshots from iCloud storage.

2. **Firebase Storage Upload**
   - Transfers the fetched screenshots to a designated Firebase Storage bucket for further processing.

3. **Text Extraction with Cloud Vision**
   - Utilizes Google Cloud Vision API to extract text from the uploaded screenshots.

4. **Categorization with GPT**
   - Uses GPT-3 to categorize the extracted text.

5. **List Creation**
   - Organizes the categorized text into lists based on the identified categories.

6. **Firestore Integration**
   - Sends the categorized data to a Firestore database for real-time access by the frontend application.

7. **Frontend Application**
   - Built with Svelte and styled with Tailwind CSS.
   - Pulls the categorized data from the Firestore database in real-time and displays it to the user.

## Technologies Used

- **Firebase Services**:
  - Firebase Storage: Storing screenshots in Firebase Storage buckets.
  - Cloud Functions: Orchestrating the workflow.
  - Firestore: NoSQL database for storing categorized data.
  - Firebase Hosting: Host and scale the frontend 
- **Google Cloud Vision API**: Extracting text from screenshots.
- **GPT**: Categorizing extracted text.
- **Svelte**: JavaScript framework for building the frontend application.
- **Tailwind CSS**: Utility-first CSS framework for styling the frontend.

## Usage

- Configure the system to fetch screenshots from iCloud periodically.
- Access the frontend application to view the categorized lists generated from the extracted text in real-time.

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
