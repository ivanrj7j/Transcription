from flask import Blueprint, request
from src.modules import Transcriber
import whisper
import json
import os
from src.api.utils import audioPresent, tempFile

restAPI = Blueprint("restAPI", __name__)

modelName = "base"
tempDirPath = "temp"

model = whisper.load_model(modelName)
trans = Transcriber(model)

@restAPI.route('/transcribe', methods=['POST'])
@audioPresent
def transcribe():
    """
    Transcribes an audio file and returns the transcription.

    Parameters:
    audio (flask.FileStorage): The uploaded audio file.

    Returns:
    str: A JSON response containing the transcription and status code.
         If an error occurs during transcription, the response will contain an error message and status code 500.
    """
    audio = request.files["audio"]

    try:
        fileName = tempFile(audio, tempDirPath)
        # saving the file 

        transcription = trans.getTranscription(fileName)
        # transcribing audio 

        os.remove(fileName)
        # removing the tempfile 

    except Exception as e:
        return json.dumps({"error":f"Can't read audio file due to [{e}]", "status":500}), 500

    return json.dumps({"transcription": transcription, "status":200}), 200


@restAPI.route('/text', methods=['POST'])
@audioPresent
def text():
    """
    Extracts text from an uploaded audio file and returns it as a JSON response.

    Parameters:
    audio (flask.FileStorage): The uploaded audio file.

    Returns:
    tuple: A JSON response containing the extracted text and status code.
         If an error occurs during extraction, the response will contain an error message and status code 500.
    """
    audio = request.files["audio"]

    try:
        fileName = tempFile(audio, tempDirPath)
        # saving the file

        text = trans.getText(fileName)
        # getting text from audio

        os.remove(fileName)
        # removing the tempfile

    except Exception as e:
        return json.dumps({"error":f"Can't read audio file due to [{e}]", "status":500}), 500

    return json.dumps({"text": text, "status":200}), 200

@restAPI.route('/rawSegments', methods=['POST'])
@audioPresent
def rawSegments():
    """
    Extracts raw audio segments from an uploaded audio file and returns them as a JSON response.

    Parameters:
    audio (flask.FileStorage): The uploaded audio file.

    Returns:
    tuple: A JSON response containing the extracted raw audio segments and status code.
         If an error occurs during extraction, the response will contain an error message and status code 500.
    """
    audio = request.files["audio"]
    
    try:
        fileName = tempFile(audio, tempDirPath)
        # saving the file 

        rawSegments = trans.getRawOutput(fileName)["segments"]
        # getting raw segments from audio 

        os.remove(fileName)
        # removing the tempfile 

    except Exception as e:
        return json.dumps({"error":f"Can't read audio file due to [{e}]", "status":500}), 500
    
    return json.dumps({"rawSegments": rawSegments, "status":200}), 200