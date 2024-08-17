# Transcription and Video Subtitling API

This project is a Flask-based application that utilizes the Whisper library for transcribing audio files and adds functionality for video subtitling. The main components of the project are the API endpoints, the Whisper model, the Transcriber class, and the video subtitling modules.

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Usage](#usage)
4. [API Endpoints](#api-endpoints)
5. [Whisper Model](#whisper-model)
6. [Transcriber Class](#transcriber-class)
7. [Video Subtitling](#video-subtitling)
8. [Utils Module](#utils-module)
9. [Main Module](#main-module)
10. [Contributing](#contributing)
11. [License](#license)

## Introduction

This project is a comprehensive solution for transcribing audio files using the Whisper library and adding subtitles to videos. It provides a set of API endpoints for audio transcription and includes modules for video subtitling. The project encompasses audio transcription, text extraction, and video subtitling functionalities.

## Tutorial

Click [here](https://github.com/ivanrj7j/Transcription/wiki/Tutorial) to see the tutorials for this project.

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

The project provides three main API endpoints for audio transcription:

- `/transcribe`: Transcribes an audio file and returns the transcription as a JSON response.
- `/text`: Extracts text from an uploaded audio file and returns it as a JSON response.
- `/rawSegments`: Extracts raw audio segments from an uploaded audio file and returns them as a JSON response.

## Whisper Model

The Whisper model is a state-of-the-art speech-to-text library used for transcribing audio files.

## Transcriber Class

The [Transcriber](src/modules/transcriber.py) class encapsulates the functionality of the Whisper model, providing methods for transcription and text extraction.

## Video Subtitling

The project includes video subtitling capabilities with two new modules:

### VideoTranscriber (video.py)

The `VideoTranscriber` class in `video.py` handles the process of adding subtitles to videos. Key features include:

- Initializing with a video file, subtitle configuration, and raw subtitle data
- Converting timestamps to frame indices
- Interpreting SRT-like subtitle data
- Applying subtitles to video frames
- Saving the subtitled video to a file

### Subtitle and SubtitleConfig (subtitle.py)

The `subtitle.py` module contains two main classes:

1. `SubtitleConfig`: Manages the configuration for subtitle appearance, including font, size, color, and positioning.

2. `Subtitle`: Represents individual subtitle segments and handles the rendering of subtitles on video frames.

These classes work together to provide a flexible and customizable video subtitling system.

## Utils Module

The `utils` module contains helper functions used throughout the project, including audio file handling and temporary file management.

## Main Module

The `main` module initializes the Flask application, registers the API endpoints, and sets up the Whisper model and Transcriber class.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.