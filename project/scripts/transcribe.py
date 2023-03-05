# Joemar
# February 22, 2023

import os
import whisper

def to_text(audio):
    
    # if audio has no-value
    if not audio:
        return "no transcribed text."
    
    # get audio file from temp data by specifying the name of audio from db
    temp_data_folder = os.getcwd() + "/project/temp_data/"
    audio = temp_data_folder + audio
    
    # text holder
    text = ""
    
    try:
        model = whisper.load_model('base')
        result = model.transcribe(
            audio,
            fp16=False,
            language='English',
            task='Translate'
        )
        readed_text = str(result["text"])
        readed_text = str(readed_text).split('.')
        for a in readed_text:
            if a != '':
                text = ' '.join(a.split())
    except Exception as e:
        ...
    
    # checking string text
    return text if not len(text) == 0 else "no transcribed text."