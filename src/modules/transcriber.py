from whisper.model import Whisper
from io import BytesIO
from src.modules.utils import encodeSegment

class Transcriber:
    def __init__(self, model:Whisper) -> None:
        self.model = model

    def getRawOutput(self, audioFile:str|BytesIO) -> dict[str, str|list]:
        return self.model.transcribe(audioFile)

    def getText(self, audioFile:str|BytesIO) -> str:
        return self.getRawOutput(audioFile)["text"]

    def getTranscription(self, audioFile:str|BytesIO) -> str:
        segments = self.getRawOutput(audioFile)["segments"]
        transcription = ""

        for i, segment in enumerate(segments):
            transcription += encodeSegment(segment, i+1)
        return transcription        

    def saveTranscription(self, transcription:str, outputFile:str):
        with open(outputFile, 'w') as f:
            f.write(transcription)

    def saveTranscriptionFromAudio(self, audioFile:str|BytesIO, outputFile:str):
        transcription = self.getTranscription(audioFile)
        self.saveTranscription(transcription, outputFile)