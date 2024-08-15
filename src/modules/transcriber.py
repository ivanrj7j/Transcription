from whisper.model import Whisper
from src.modules.utils import encodeSegment

class Transcriber:
    def __init__(self, model: Whisper) -> None:
        """
        Initialize the Transcriber class with a Whisper model.

        Args:
        model (Whisper): A Whisper model instance for transcribing audio files.

        Returns:
        None
        """
        self.model = model

    def getRawOutput(self, audioFile: str) -> dict[str, str | list]:
        """
        Retrieve the raw output from the Whisper model's transcription of the given audio file.

        Args:
        audioFile (str): The path to the audio file to be transcribed.

        Returns:
        dict[str, str | list]: A dictionary containing the raw output from the Whisper model's transcription. The dictionary keys are "text" and "segments", where "text" contains the full transcription and "segments" contains the transcription broken down into segments.
        """
        return self.model.transcribe(audioFile)

    def getText(self, audioFile: str) -> str:
        """
        Retrieve the full transcription text from the Whisper model's transcription of the given audio file.

        Args:
        audioFile (str): The path to the audio file to be transcribed.

        Returns:
        str: The full transcription text obtained from the Whisper model's transcription of the audio file.
        """
        return self.getRawOutput(audioFile)["text"]

    def getTranscription(self, audioFile:str) -> str:
        """
        Retrieve the full transcription text from the Whisper model's transcription of the given audio file,
        broken down into segments and then combined into a single transcription.

        Args:
        audioFile (str): The path to the audio file to be transcribed.

        Returns:
        str: The full transcription text obtained from the Whisper model's transcription of the audio file,
        broken down into segments and then combined into a single transcription.
        """
        segments = self.getRawOutput(audioFile)["segments"]
        transcription = ""

        for i, segment in enumerate(segments):
            transcription += encodeSegment(segment, i+1)
        return transcription        

    def saveTranscription(self, transcription: str, outputFile: str) -> None:
        """
        Save the transcription text to a file.

        Args:
        transcription (str): The full transcription text obtained from the Whisper model's transcription of the audio file.
        outputFile (str): The path to the file where the transcription will be saved.

        Returns:
        None

        This function saves the transcription text to a file specified by the 'outputFile' parameter. The transcription text is written to the file in its entirety.
        """
        with open(outputFile, 'w') as f:
            f.write(transcription)

    def saveTranscriptionFromAudio(self, audioFile: str, outputFile: str) -> None:
        """
        Save the transcription text to a file, obtained from transcribing the given audio file.

        Args:
        audioFile (str): The path to the audio file to be transcribed.
        outputFile (str): The path to the file where the transcription will be saved.

        Returns:
        None

        This function saves the transcription text to a file specified by the 'outputFile' parameter. The transcription text is written to the file in its entirety. The transcription text is obtained by transcribing the audio file using the 'getTranscription' method, which breaks down the transcription into segments and then combines them into a single transcription.
        """
        transcription = self.getTranscription(audioFile)
        self.saveTranscription(transcription, outputFile)