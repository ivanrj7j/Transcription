from decord import VideoReader
from typing import Generator
from src.modules.utils import newLineText
from src.modules.subtitle import SubtitleConfig, Subtitle
from numpy import ndarray
import cv2
from tqdm import tqdm

class VideoTranscriber:
    def __init__(self, video:VideoReader, subConfig:SubtitleConfig, rawSubtitles:dict[str, str|int|float|list]) -> None:
        """
        Initialize the VideoTranscriber object.

        Args:
            video (VideoReader): A VideoReader object containing the video frames.
            subConfig (SubtitleConfig): A SubtitleConfig object containing the configuration for the subtitles.
            rawSubtitles (dict[str, str | int | float | list]): A dictionary containing raw subtitle data.

        Returns:
            None. Initializes the VideoTranscriber object with the provided video, subtitle configuration, and raw subtitle data.
        """
        self.video = video
        self.fps = round(video.get_avg_fps())
        self.subConfig = subConfig

        videoShape = self.video[0].shape
        self.subConfig.screenShape = (videoShape[1], videoShape[0])

        self.subList = list(self.interpretSRT(rawSubtitles))

    @classmethod
    def fromFile(cls, fileName:str, subConfig:SubtitleConfig, rawSubtitles:dict[str, str|int|float|list]):
        """
        Create and initialize a VideoTranscriber object from a video file.

        Args:
            fileName (str): The path to the video file.
            subConfig (SubtitleConfig): A SubtitleConfig object containing the configuration for the subtitles.
            rawSubtitles (dict[str, str | int | float | list]): A dictionary containing raw subtitle data.

        Returns:
            VideoTranscriber: A VideoTranscriber object initialized with the provided video file, subtitle configuration, and raw subtitle data.
        """
        video = VideoReader(fileName)
        return cls(video, subConfig, rawSubtitles)
    
    @staticmethod
    def interpretSegment(segment:dict[str, str|float|list|int]):
        """
        Interpret a single subtitle segment from the raw subtitle data.

        Args:
            segment (dict[str, str | float | list | int]): A dictionary containing the start, end, and text of a subtitle segment.

        Returns:
            tuple[float, float, str]: A tuple containing the start time, end time, and text of the interpreted subtitle segment.
        """
        return segment["start"], segment["end"], segment["text"]
    
    def timeStamp2Frame(self, timestamp:float):
        """
        Convert a timestamp to a frame index.

        Args:
            timestamp (float): The timestamp in seconds.

        Returns:
            int: The frame index corresponding to the given timestamp.

        This method takes a timestamp in seconds and converts it to a frame index using the video's frame rate (fps). The frame index is calculated by multiplying the timestamp by the frame rate and rounding the result.
        """
        return round(self.fps * timestamp)

    def interpretSRT(self, segments:list[dict[str, str|float|list|int]]):
        """
        Interpret the raw subtitle data and generate a sequence of Subtitle objects.

        Args:
            segments (list[dict[str, str | float | list | int]]): A list of dictionaries containing the raw subtitle data. Each dictionary should have keys 'start', 'end', and 'text', representing the start time, end time, and text of a subtitle segment, respectively.

        Yields:
            Subtitle: A Subtitle object representing a subtitle segment with its start and end frames, text, and configuration.

        This method iterates through the provided list of subtitle segments, interprets each segment by converting its start and end times to frame indices, and generates a sequence of Subtitle objects. Each Subtitle object is yielded as it is generated, allowing the caller to process each subtitle segment individually.
        """
        for segment in segments:
            start, end, text = VideoTranscriber.interpretSegment(segment)
            startFrame = self.timeStamp2Frame(start)
            endFrame = self.timeStamp2Frame(end)
            text = newLineText(text, self.subConfig.newLineInterval)
            yield Subtitle(text, self.subConfig, startFrame, endFrame)

    def handleFrame(self, frame:ndarray, i:int, currentInterpreterIndex:int):
        """
        Process a single frame of the video and apply subtitles if necessary.

        Args:
            frame (ndarray): The current frame of the video.
            i (int): The index of the current frame.
            currentInterpreterIndex (int): The current index of the subtitle segment being interpreted.

        Returns:
            Tuple[ndarray, int]: A tuple containing the processed frame and the updated currentInterpreterIndex.

        This method takes a frame from the video, converts it to a NumPy array, and applies the appropriate subtitle segment if the current frame falls within the start and end times of the current subtitle segment. If the current frame is at the start of a new subtitle segment, the currentInterpreterIndex is updated to point to the new subtitle segment. The processed frame and the updated currentInterpreterIndex are returned as a tuple.
        """
        frame = frame.asnumpy()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        totalSubs = len(self.subList)

        if currentInterpreterIndex < totalSubs:
            if i >= self.subList[currentInterpreterIndex].start and i < self.subList[currentInterpreterIndex].end:
                frame = self.subList[currentInterpreterIndex].draw(frame)

            elif currentInterpreterIndex + 1 < totalSubs:
                if i == self.subList[currentInterpreterIndex+1].start:
                    currentInterpreterIndex += 1

        return frame, currentInterpreterIndex
    
    def subtitle(self, outputPath:str, verbose=False, outputFourcc:int=cv2.VideoWriter_fourcc(*'mp4v')):
        """
        Apply subtitles to the video and save the result to a new video file.

        Args:
            outputPath (str): The path to save the output video file.
            verbose (bool, optional): If True, display a progress bar during the subtitling process. Defaults to False.
            outputFourcc (int, optional): The four-character code for the output video format. Defaults to cv2.VideoWriter_fourcc(*'mp4v').

        Returns:
            None. The function applies subtitles to the video and saves the result to a new video file.
        """
        writer = cv2.VideoWriter(outputPath, outputFourcc, self.fps, self.subConfig.screenShape)

        currentInterpreterIndex = 0
        loop =  enumerate(self.video)

        if verbose:
            loop = tqdm(loop, total=len(self.video), unit=" frames")

        for i, frame in loop:

            frame, currentInterpreterIndex = self.handleFrame(frame, i, currentInterpreterIndex)

            writer.write(frame)
            

        writer.release()

    