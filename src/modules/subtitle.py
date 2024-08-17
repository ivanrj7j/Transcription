from cv2 import getTextSize, putText
from numpy import ndarray

class SubtitleConfig:
    def __init__(self, fontFamily, scale:float, thickness:float, lineSpacing:int|float, color:tuple[int, int, int], relativePos:tuple[int, int]=(0.5, 0.5), screenShape:tuple[int, int]=(640, 290), newLineInterval=8) -> None:
        """
        Initialize a SubtitleConfig object with the given parameters.

        Parameters:
        fontFamily (str): The font family to be used for rendering subtitles.
        scale (float): The scale factor for the font size.
        thickness (float): The thickness of the font strokes.
        lineSpacing (int|float): The spacing between lines of subtitles.
        color (tuple[int, int, int]): The RGB color code for the subtitle text.
        relativePos (tuple[int, int], optional): The relative position of the subtitle on the screen. Default is (0.5, 0.5), which represents the center.
        screenShape (tuple[int, int], optional): The shape of the screen in pixels. Default is (640, 290).

        Returns:
        None
        """
        self.fontFamily = fontFamily
        self.scale = scale
        self.thickness = thickness
        self.lineSpacing = lineSpacing
        self.color = color
        self.relativePos = relativePos
        self.screenShape = screenShape
        self.newLineInterval = newLineInterval

    @property
    def position(self):
        x, y = self.screenShape[0]*self.relativePos[0], self.screenShape[1]*self.relativePos[1]
        return round(x), round(y)
    
    def __str__(self) -> str:
        return f"SubtitleConfig({self.position})"


class Subtitle:
    def __init__(self, text:str, config:SubtitleConfig, start:int, end:int) -> None:
        """
        Initialize a Subtitle object with the given text and configuration.

        Parameters:
        text (str): The text to be displayed as a subtitle.
        config (SubtitleConfig): An instance of the SubtitleConfig class containing the configuration parameters for rendering the subtitle.
        start (int): The start time of the subtitle (frame number).
        end (int): The end time of the subtitle (frame number).

        Returns:
        None
        """
        self.text = text
        self.config = config
        self.start = start
        self.end = end
    
    def calculateAnchor(self, x:int, y:int, text:str):
        """
        Calculate the anchor point for rendering the subtitle on the screen.

        Parameters:
        - x (int): The x-coordinate of the top-left corner of the subtitle on the screen.
        - y (int): The y-coordinate of the top-left corner of the subtitle on the screen.

        Returns:
        - A tuple (x, y) representing the anchor point for rendering the subtitle on the screen.

        The anchor point is calculated based on the position of the subtitle on the screen and the size of the text. The position is determined by the configuration parameters specified in the SubtitleConfig instance passed to the Subtitle object. The size of the text is obtained using the getTextSize function from the OpenCV library. The anchor point is then calculated as the center of the text, which is halfway between the left and right edges, and halfway between the top and bottom edges.
        """
        w, h = getTextSize(text, self.config.fontFamily, self.config.scale, self.config.thickness)[0]
        u, v = round(w/2), round(h/2)

        x, y = x-u, y-v
        return x, y

    def draw(self, frame:ndarray):
        """
        Draw the subtitle on the given frame.

        Parameters:
        - frame (ndarray): The input frame on which the subtitle will be rendered.

        Returns:
        - ndarray: The frame with the subtitle rendered on it.

        This function takes an input frame and renders the subtitle on it according to the configuration specified in the SubtitleConfig instance. The subtitle is rendered at the position specified in the configuration, with the specified font family, scale, thickness, line spacing, and color. If the subtitle text contains multiple lines, they are rendered one after the other with the specified line spacing. The function returns the frame with the rendered subtitle.
        """
        x, y = self.config.position
        if "\n" not in self.text:
            anchorX, anchorY = self.calculateAnchor(x, y, self.text)
            putText(frame, self.text, (anchorX, anchorY), self.config.fontFamily, self.config.scale, self.config.color, self.config.thickness)
        else:
            for line in self.text.split("\n"):
                anchorX, anchorY = self.calculateAnchor(x, y, line)
                putText(frame, line, (anchorX, anchorY), self.config.fontFamily, self.config.scale, self.config.color, self.config.thickness)
                y += self.config.lineSpacing
        return frame
    
    def __str__(self) -> str:
        return self.text
    
    def __repr__(self) -> str:
        return f"Subtitle(text={self.text}, start={self.start}, end={self.end})"