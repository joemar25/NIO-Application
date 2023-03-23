from EmotionDetector import EmotionDetector
import os

detector = EmotionDetector()
audio_path = os.getcwd() + "/project/temp_data/23322b4e7711e-c8a2-11ed-a657-708bcd015b0c111426.wav"
predictions = detector.predict_emotion(audio_path)
print(predictions)
