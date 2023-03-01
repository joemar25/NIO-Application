# John Olan S. Gomez | Joemar
# Finding the rate of the speech
# 02-27-2023

import librosa

__LOWEST_IDEAL = 2.33
__HIGHEST_IDEAL = 2.67
__REDUCTION = 0.0683 / 0.17
__IDEAL_SCORE = 100

def get_rate(audio_file, text_data): 
    
    audioDuration =  float(librosa.get_duration(filename=(audio_file)))
    wordList      =  str.split(text_data)
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
        
    #determine speed of the speech
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
        "rating": speechRating,
    }
