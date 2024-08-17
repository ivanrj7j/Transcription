from cv2 import getTextSize, putText, rectangle
from numpy import ndarray
from PIL.ImageFont import FreeTypeFont, truetype
from PIL import Image, ImageDraw
from numpy import array

class SubtitleConfig:
    def __init__(self, fontFamily:int|str, scale:float, thickness:float, lineSpacing:int|float, color:tuple[int, int, int], relativePos:tuple[int, int]=(0.5, 0.5), screenShape:tuple[int, int]=(640, 290), newLineInterval:int=8, backBox:bool=True, backBoxColor:tuple[int, int, int]=(60, 170, 250), padding:int=2) -> None:
        """
        Initialize a SubtitleConfig object with the given parameters.

        Parameters:
        fontFamily (int| str): The font family of the text.
        scale (float): The scale factor for the font size.
        thickness (float): The thickness of the font strokes.
        lineSpacing (int|float): The spacing between lines of subtitles.
        color (tuple[int, int, int]): The RGB color code for the subtitle text.
        relativePos (tuple[int, int], optional): The relative position of the subtitle on the screen. Default is (0.5, 0.5), which represents the center.
        screenShape (tuple[int, int], optional): The shape of the screen in pixels. Default is (640, 290).
        newLineInterval (int, optional): The maximum number of words per line in the subtitle. Default is 8.
        backBox (bool, optional): Whether to draw a background box around the subtitle. Default is False.
        backBoxColor (tuple[int, int, int], optional): The RGB color code for the background box. Default is (60, 170, 250).
        padding (int, optional): The padding around the subtitle text. Default is 2.

        Returns:
        None
        """
        self.offsetDirection = 1
        # deals with the direction of the offest 1 for opencv and -1 for PIL

        self.fontFamily = fontFamily
        if isinstance(fontFamily, str):
            self.fontFamily = truetype(fontFamily, scale)
            self.offsetDirection = -1

        self.scale = scale
        self.thickness = thickness
        self.lineSpacing = lineSpacing
        self.relativePos = relativePos
        self.screenShape = screenShape

        self.color = color

        self.newLineInterval = newLineInterval

        self.backBox = backBox

        r,g,b = backBoxColor
        self.backBoxColor = (b, g, r)

        self.padding = padding

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
    
    def getTextDimensions(self, text:str):
        if isinstance(self.config.fontFamily, FreeTypeFont):
            image = Image.new('RGB', (1, 1))
            draw = ImageDraw.Draw(image)

            # Get bounding box of the text
            bbox = draw.textbbox((0, 0), text, font=self.config.fontFamily)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
            return w, h
        
        return getTextSize(text, self.config.fontFamily, self.config.scale, self.config.thickness)[0]
    
    def calculateAnchor(self, x:int, y:int, text:str):
        """
        Calculate the anchor point for rendering the subtitle on the screen.

        Parameters:
        - x (int): The x-coordinate of the top-left corner of the subtitle on the screen.
        - y (int): The y-coordinate of the top-left corner of the subtitle on the screen.

        Returns:
        - A tuple (x, y) representing the anchor point for rendering the subtitle on the screen.
        - A tuple (w, h) representing the width and height of text.

        The anchor point is calculated based on the position of the subtitle on the screen and the size of the text. The position is determined by the configuration parameters specified in the SubtitleConfig instance passed to the Subtitle object. The size of the text is obtained using the getTextSize function from the OpenCV library. The anchor point is then calculated as the center of the text, which is halfway between the left and right edges, and halfway between the top and bottom edges.
        """
        w, h = self.getTextDimensions(text)
        u, v = round(w/2), round(h/2)

        x, y = x-u, y-v
        return (x, y), (w, h)
    
    def darwBackBox(self, frame:ndarray, anchorX:int, anchorY:int, width:int, height:int):
        if not self.config.backBox:
            return frame
        
        offset = 2*self.config.padding

        x1, y1 = anchorX-offset, anchorY+offset*self.config.offsetDirection
        x2, y2 = anchorX+(width+offset), anchorY-(height+offset)*self.config.offsetDirection
        frame = rectangle(frame, (x1, y1), (x2, y2), self.config.backBoxColor, -1)

        return frame
    
    def renderText(self, text:str, x:int, y:int, frame:ndarray):
        if isinstance(self.config.fontFamily, FreeTypeFont):
            image = Image.fromarray(frame)
            draw = ImageDraw.Draw(image)
            draw.text((x, y), text, font=self.config.fontFamily, fill=self.config.color)
            return array(image)
        
        return putText(frame, text, (x, y), self.config.fontFamily, self.config.scale, self.config.color, self.config.thickness)

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
            (anchorX, anchorY), (w, h) = self.calculateAnchor(x, y, self.text)
            frame = self.darwBackBox(frame, anchorX, anchorY, w, h)
            frame = self.renderText(self.text, anchorX, anchorY, frame)
            # handling single line subtitle 
        else:
            boxData = []
            lines = self.text.split("\n")

            for line in lines:
                (anchorX, anchorY), (w, h) = self.calculateAnchor(x, y, line)
                boxData.append(((anchorX, anchorY), (w, h), line))
                y += self.config.lineSpacing
            
            for (anchorX, anchorY), (w, h), line in boxData:
                frame = self.darwBackBox(frame, anchorX, anchorY, w, h) 

            for (anchorX, anchorY), (w, h), line in boxData:
                frame = self.renderText(line, anchorX, anchorY, frame)

            # handling multi line subtitle 
            # did three for loops instead of one to avoid text and box overlap            
        return frame
    
    def __str__(self) -> str:
        return self.text
    
    def __repr__(self) -> str:
        return f"Subtitle(text={self.text}, start={self.start}, end={self.end})"