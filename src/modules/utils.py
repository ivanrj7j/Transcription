def SRTTime(_seconds:str):
    _seconds = float(_seconds)
    hours, remainder = divmod(_seconds, 3600)
    minutes, remainder = divmod(remainder, 60)
    seconds, ms = divmod(remainder, 1)
    ms = round(ms*1e3)
    
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{ms}"

def encodeSegment(segment:dict[str, int|list|float|str], i:int, newLineInterval:int=8):
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