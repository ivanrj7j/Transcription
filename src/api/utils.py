from flask import request
import json
from uuid import uuid1
# from werkzeug.datastructures import FileStorage
import os
from functools import wraps

def audioPresent(func):
    @wraps(func)
    def decoratedFunc():
        if "audio" not in request.files:
            return json.dumps({"error":"Audio file not found", "status":404}), 404
        return func()
    
    return decoratedFunc

def tempFile(file, dst:str):
    fileID = str(uuid1())
    fileExtension = file.filename.split(".")[-1]
    fileName = os.path.join(dst, f"{fileID}.{fileExtension}")

    file.save(fileName)

    return fileName