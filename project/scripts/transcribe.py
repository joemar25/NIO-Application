# Joemar
# February 22, 2023

import whisper

__MODEL = 'base'
 
def to_text(audio_file) : 
    
    audio_file = r"{audio_file}"
    # text holder
    text = ""
    
    try:
        model = whisper.load_model(__MODEL)
        result = model.transcribe(
            audio_file,
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
        
    