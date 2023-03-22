# Joemar
# February 22, 2023

import os
import whisper

def to_text(audio, use_temp_folder=True):
    
    # if audio has no-value
    if not audio:
        return "no transcribed text."
    
    # get audio file from temp data by specifying the name of audio from db
    text = temp_data_folder = ''
    if use_temp_folder:
        temp_data_folder = temp_data_folder = os.getcwd() + "/project/temp_data/"
    audio = temp_data_folder + audio
    
    try:
        model = whisper.load_model('base')
        result = model.transcribe(
            audio,
            fp16=False,
            language='English',
            task='Translate'
        )
        
        readed_text = str(result["text"])
        text = readed_text.strip()
       
    except Exception as e:
        ...
    
    # checking string text
    return text if not len(text) == 0 else "no transcribed text."