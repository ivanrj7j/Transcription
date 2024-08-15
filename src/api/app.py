from flask import Blueprint, request
from src.modules import Transcriber
import whisper
from uuid import uuid1
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