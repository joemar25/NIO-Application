# John Olan S. Gomez
# Joemar
# Finding the rate of the speech
# 02-27-2023

import os
import whisper
import librosa

def get_rate(audio_file, text_data) : 
    
    LOWEST_IDEAL = 2.33
    HIGHEST_IDEAL = 2.67
    REDUCTION = 0.0683 / 0.17
    IDEAL_SCORE = 100

    model = whisper.load_model('base')

    result = model.transcribe(
        audio_file,
        fp16=False,
        language='English',
        task='Translate'
    )

    audioDuration= float(librosa.get_duration(filename=(audio_file)))
    sentence= str(result["text"])
    wordList= str.split(sentence)
    wordNum= int(len(wordList))
    rate= wordNum/audioDuration
    wpm= rate*60

    # calculate speech score
    if rate<LOWEST_IDEAL:
        speechScore= LOWEST_IDEAL - rate
        speechScore= speechScore * REDUCTION
        speechScore= IDEAL_SCORE - speechScore
    elif rate>HIGHEST_IDEAL:
        speechScore = rate - HIGHEST_IDEAL
        speechScore = speechScore * REDUCTION
        speechScore = IDEAL_SCORE - speechScore

    else:
        speechScore= IDEAL_SCORE



    #determine speed of the speech
    speechRating = ""
    if wpm < 140:
        speechRating = "Slow"
    elif wpm >= 140 and wpm <=160:
        speechRating = "Ideal"
    else:
        speechRating = "Fast"

    print("Audio duration: ", audioDuration)
    print("Number of words in sentence:", wordNum)
    print("Speech score: %.2f%%" % speechScore)
    print("Speech rate: %.2f wpm" % wpm)
    print("Your speech rate is:", speechRating)
    print(sentence)
    

audio_title = '\sample.wav' # change this audio file
audio_path = os.getcwd() + audio_title
print()
print()
print(audio_path)
print()
print()
# get_rate(audio_path) # use function for testing