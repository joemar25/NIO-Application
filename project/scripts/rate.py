# Olan | Joemar
# Rate of the Speech
# Using Librosa Package

import os
import librosa

# contants
__LOWEST_IDEAL = 2.33
__HIGHEST_IDEAL = 2.67
__REDUCTION = 0.0683 / 0.17
__IDEAL_SCORE = 100

# funciton to call to get the rate score of the audio
def rate_score(audio, text, use_temp_folder=True):
    
    # if text or audio has no-value
    if not (text and audio) or text == "no transcribed text.":
        return { "score": 0, "wpm": 0, "rating": "" }
    
    # get audio file from temp data by specifying the name of audio from db
    temp_data_folder = ''
    if use_temp_folder:
        temp_data_folder = temp_data_folder = os.getcwd() + "/project/temp_data/"
    audio = temp_data_folder + audio

    """
    warning :  This alias will be removed in version 1.0.
               audioDuration =  float(librosa.get_duration(filename=(audio)))
    solution:  replace filename=(audio) -> path=(audio)
    """
    
    # librosa setup
    audioDuration =  float(librosa.get_duration(path=(audio)))
    wordList      =  str.split(text)
    wordNum       =  int(len(wordList))
    rate          =  wordNum/audioDuration
    wpm           =  rate * 60

    # calculate speech score
    if rate < __LOWEST_IDEAL:
        speechScore = __LOWEST_IDEAL - rate
        speechScore = speechScore * __REDUCTION
        speechScore = __IDEAL_SCORE - speechScore

    elif rate > __HIGHEST_IDEAL:
        speechScore = rate - __HIGHEST_IDEAL
        speechScore = speechScore * __REDUCTION
        speechScore = __IDEAL_SCORE - speechScore

    else:
        speechScore = __IDEAL_SCORE
        
    # determine speed of the speech
    speechRating = ""
    if wpm < 140:
        speechRating = "Slow"
        
    elif wpm >= 140 and wpm <= 160:
        speechRating = "Ideal"
        
    else:
        speechRating = "Fast"

    return {
        "score": speechScore,
        "wpm": wpm,
        "rating": speechRating
    }