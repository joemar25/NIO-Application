# John Olan S. Gomez
# Finding the rate of the speech
# 12-05-2022

FILE = r"C:\Users\Olan\Documents\Olan\3rd_year\CS_117-Software_Engineering_1\Prototype\rate\venv\happy_olan.wav"
LOWEST_IDEAL = 2.33
HIGHEST_IDEAL = 2.67
REDUCTION = 0.0683 / 0.17
IDEAL_SCORE = 100

import whisper
import librosa

model = whisper.load_model('base')

result = model.transcribe(
    FILE,
    fp16=False,
    language='English',
    task='Translate'
)

audioDuration= float(librosa.get_duration(filename=(FILE)))
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