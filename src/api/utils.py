from flask import request
import json
from uuid import uuid1
from werkzeug.datastructures import FileStorage
import os
from functools import wraps

def audioPresent(func):
    """
    Decorator function to check if an audio file is present in the request.
    If the audio file is not found, it returns a JSON response with an error message and status code 404.

    Parameters:
    - func (function): The function to be decorated.

    Returns:
    - decoratedFunc (function): The decorated function that checks for the presence of an audio file in the request.
    """
    @wraps(func)
    def decoratedFunc():
        if "audio" not in request.files:
            return json.dumps({"error":"Audio file not found", "status":404}), 404
        return func()
    
    return decoratedFunc

def tempFile(file, dst:str):
    """
    This function saves the provided file to a temporary location with a unique ID and extension.

    Parameters:
    - file (FileStorage): The file object to be saved.
    - dst (str): The destination directory path where the temporary file will be saved.

    Returns:
    - fileName (str): The full path of the saved temporary file.
    """
    fileID = str(uuid1())
    fileExtension = file.filename.split(".")[-1]
    fileName = os.path.join(dst, f"{fileID}.{fileExtension}")

    file.save(fileName)

    return fileName