# Transcription API

This project is a Flask-based application that utilizes the Whisper library for transcribing audio files. The main components of the project are the API endpoints, the Whisper model, and the Transcriber class.

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Usage](#usage)
4. [API Endpoints](#api-endpoints)
   - `/transcribe`
   - `/text`
   - `/rawSegments`
5. [Whisper Model](#whisper-model)
6. [Transcriber Class](#transcriber-class)
7. [Utils Module](#utils-module)
8. [Main Module](#main-module)
9. [Contributing](#contributing)
10. [License](#license)

## Introduction

This project is a complete solution for transcribing audio files using the Whisper library. It provides a set of API endpoints that allow users to transcribe audio files and extract text and raw audio segments from them. The project also includes a custom Transcriber class that encapsulates the functionality of the Whisper model and provides additional methods for saving the transcription text to a file.

## Installation

To install the project, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/ivanrj7j/Transcription.git
   ```

2. Navigate to the project directory:
   ```
   cd Transcription
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To use the project, follow these steps:

1. Start the Flask application:
   ```
   python main.py
   ```

2. The application will start on port 5000 by default. You can access the API endpoints using a tool like Postman or curl.

## API Endpoints

The project provides three main API endpoints:

- `/transcribe`: This endpoint transcribes an audio file and returns the transcription as a JSON response. It uses the [Transcriber](src/modules/transcriber.py) class to get the transcription and then returns the result.

- `/text`: This endpoint extracts text from an uploaded audio file and returns it as a JSON response. It also uses the [Transcriber](src/modules/transcriber.py) class to get the text from the audio.

- `/rawSegments`: This endpoint extracts raw audio segments from an uploaded audio file and returns them as a JSON response. It also uses the [Transcriber](src/modules/transcriber.py) class to get the raw segments from the audio.

## Whisper Model

The Whisper model is a state-of-the-art speech-to-text library that is used for transcribing audio files. The project uses the `Whisper` class from the Whisper library to perform the transcription.

## Transcriber Class

The [Transcriber](src/modules/transcriber.py) class is a custom class that encapsulates the functionality of the Whisper model. It provides methods for getting the raw output from the Whisper model's transcription, getting the full transcription text, and getting the transcription broken down into segments. The [Transcriber](src/modules/transcriber.py) class also provides a method for saving the transcription text to a file.

## Utils Module

The `utils` module contains helper functions that are used throughout the project. The `audioPresent` decorator function checks if an audio file is present in the request. The `tempFile` function saves the provided file to a temporary location with a unique ID and extension.

## Main Module

The `main` module initializes the Flask application and registers the API endpoints. It also sets up the Whisper model and the Transcriber class.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.