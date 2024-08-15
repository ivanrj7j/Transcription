def SRTTime(_seconds:str):
    """
    Converts a given number of seconds into a formatted SRT time string.

    Args:
    _seconds (str): A string representing the number of seconds.

    Returns:
    str: A string representing the time in the format HH:MM:SS,ms, where HH, MM, SS are integers and ms is a 3-digit integer.

    Example:
    >>> SRTTime("3660")
    '01:01:06,000'
    """
    _seconds = float(_seconds)
    hours, remainder = divmod(_seconds, 3600)
    minutes, remainder = divmod(remainder, 60)
    seconds, ms = divmod(remainder, 1)
    ms = round(ms*1e3)
    
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{ms}"

def encodeSegment(segment:dict[str, int|list|float|str], i:int, newLineInterval:int=8):
    """
    Encodes a given segment of text into an SRT format string.

    Args:
    segment (dict): A dictionary containing the text, start time, and end time of the segment.
        - text (str): The text content of the segment.
        - start (int | float): The start time of the segment in seconds.
        - end (int | float): The end time of the segment in seconds.
    i (int): An integer representing the index of the segment.
    newLineInterval (int, optional): The maximum number of words per line in the encoded segment. Defaults to 8.

    Returns:
    str: A string representing the encoded segment in SRT format.

    Example:
    >>> encodeSegment({'text': 'This is a sample text.', 'start': 3660, 'end': 4200}, 1)
    '1\n01:01:06,000 --> 01:02:00,000\nThis is a sample text.\n\n'
    """
    text = segment['text']
    start = SRTTime(segment['start'])
    end = SRTTime(segment['end'])

    splitText = text.split()
    if len(splitText) > newLineInterval:
        for wordIndex, word in enumerate(splitText):
            if wordIndex % (newLineInterval-1) == 0 and wordIndex > 0:
                splitText[wordIndex] = word + '\n'
            else:
                splitText[wordIndex] = word + " "

        text = "".join(splitText)

    return f"{i}\n{start} --> {end}\n{text}\n\n"