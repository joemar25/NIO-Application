import os, librosa, joblib, numpy as np
from keras.models import load_model

class EmotionDetector:
    def __init__(self):
        file_loc = os.getcwd() + "/project/scripts/emotion/"

        # Load the model, scaler, and encoder
        self.model = load_model(file_loc + "emotion_detect.h5")
        self.scaler = joblib.load(file_loc + "scaler.pkl")
        self.encoder = joblib.load(file_loc + "encoder.pkl")

    def predict(self, audio_path):
        data, sample_rate = librosa.load(audio_path)

        # Extract features and transform with the scaler
        features = self.scaler.transform(self.extract_features(data, sample_rate).reshape(1, -1))

        # Predict the emotions
        pred_test = self.model.predict(np.expand_dims(features, axis=2), verbose=0)[0]

        # Combine into a dictionary
        emotion_dict = dict(zip(self.encoder.categories_[0], pred_test))

        # Sort emotions by confidence level
        sorted_emotions = sorted(emotion_dict.items(), key=lambda x: x[1], reverse=True)

        # Return top 3 detected emotions in an array with their confidence score
        return [(emotion, "{:.2f}".format(score * 100)) for (emotion, score) in sorted_emotions[:3]]

    def extract_features(self, data, sample_rate):
        # ZCR
        result = np.mean(librosa.feature.zero_crossing_rate(y=data).T, axis=0)

        # Chroma_stft
        stft = np.abs(librosa.stft(data))
        chroma_stft = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)

        # MFCC
        mfcc = np.mean(librosa.feature.mfcc(y=data, sr=sample_rate).T, axis=0)

        # Root Mean Square Value
        rms = np.mean(librosa.feature.rms(y=data).T, axis=0)

        # MelSpectogram
        mel = np.mean(librosa.feature.melspectrogram(y=data, sr=sample_rate).T, axis=0)

        # Return concatenate all the features
        return np.concatenate([result, chroma_stft, mfcc, rms, mel])

# with demo test
# detector = EmotionDetector()
# audio_path = os.getcwd() + "/project/temp_data/your_wave_filename.wav"
# predictions = detector.predict(audio_path)
# print(predictions)


