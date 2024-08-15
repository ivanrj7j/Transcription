from flask import Flask, request
from src.modules import Transcriber
import whisper
from uuid import uuid1
import json
import os
from base64 import b64encode

restAPI = Flask(__name__)

modelName = "base"
tempDirPath = "temp"

model = whisper.load_model(modelName)
trans = Transcriber(model)


@restAPI.route('/transcribe', methods=['POST'])
def transcribe():
    if "audio" not in request.files:
        return json.dumps({"error":"Audio file not found", "status":404}), 404
    
    audio = request.files["audio"]
    
    try:
        fileID = str(uuid1())
        fileExtension = audio.filename.split(".")[-1]
        fileName = os.path.join(tempDirPath, f"{fileID}.{fileExtension}")
        audio.save(fileName)
        # saving the file 

        transcription = trans.getTranscription(fileName)
        # transcribing audio 

        os.remove(fileName)
        # removing the tempfile 

    except Exception as e:
        return json.dumps({"error":f"Can't read audio file due to [{e}]", "status":500}), 500
    
    return json.dumps({"transcription": transcription, "status":200}), 200
