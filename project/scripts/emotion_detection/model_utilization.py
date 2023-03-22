# John Olan S. Gomez
# BSCS 3A
# March 22, 2023
# Speech Emotion Detection - Using the model to make predictions
# Software Engineering Final Project

import pandas as pd
import numpy as np

# librosa is a Python library for analyzing audio and music. It can be used to extract the data from the audio files we will see it later.
import librosa
import librosa.display

from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split

from keras.models import Sequential
from keras.layers import Dense, Conv1D, MaxPooling1D, Flatten, Dropout

Features = pd.read_csv(r"/scripts/emotion_detection/features.csv")
# Data Preparation - splitting the data for training and testing
X = Features.iloc[: ,:-1].values
Y = Features['labels'].values

# As this is a multiclass classification problem onehotencoding our Y.
encoder = OneHotEncoder()
Y = encoder.fit_transform(np.array(Y).reshape(-1,1)).toarray()

# splitting data
x_train, x_test, y_train, y_test = train_test_split(X, Y, random_state=0, shuffle=True)
x_train.shape, y_train.shape, x_test.shape, y_test.shape

# scaling our data with sklearn's Standard scaler
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)
x_train.shape, y_train.shape, x_test.shape, y_test.shape

# making our data compatible to model.
x_train = np.expand_dims(x_train, axis=2)
x_test = np.expand_dims(x_test, axis=2)
x_train.shape, y_train.shape, x_test.shape, y_test.shape

# Modelling
model = Sequential()
model.add(Conv1D(256, kernel_size=5, strides=1, padding='same', activation='relu', input_shape=(x_train.shape[1], 1)))
model.add(MaxPooling1D(pool_size=5, strides = 2, padding = 'same'))

model.add(Conv1D(256, kernel_size=5, strides=1, padding='same', activation='relu'))
model.add(MaxPooling1D(pool_size=5, strides = 2, padding = 'same'))

model.add(Conv1D(128, kernel_size=5, strides=1, padding='same', activation='relu'))
model.add(MaxPooling1D(pool_size=5, strides = 2, padding = 'same'))
model.add(Dropout(0.2))

model.add(Conv1D(64, kernel_size=5, strides=1, padding='same', activation='relu'))
model.add(MaxPooling1D(pool_size=5, strides = 2, padding = 'same'))

model.add(Flatten())
model.add(Dense(units=32, activation='relu'))
model.add(Dropout(0.3))

model.add(Dense(units=8, activation='softmax'))
model.compile(optimizer = 'adam' , loss = 'categorical_crossentropy' , metrics = ['accuracy'])

# Feature extraction
def extract_features(data, sample_rate):
    # ZCR
    result = np.array([])
    zcr = np.mean(librosa.feature.zero_crossing_rate(y=data).T, axis=0)
    result = np.hstack((result, zcr))  # stacking horizontally

    # Chroma_stft
    stft = np.abs(librosa.stft(data))
    chroma_stft = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
    result = np.hstack((result, chroma_stft))  # stacking horizontally

    # MFCC
    mfcc = np.mean(librosa.feature.mfcc(y=data, sr=sample_rate).T, axis=0)
    result = np.hstack((result, mfcc))  # stacking horizontally

    # Root Mean Square Value
    rms = np.mean(librosa.feature.rms(y=data).T, axis=0)
    result = np.hstack((result, rms))  # stacking horizontally

    # MelSpectogram
    mel = np.mean(librosa.feature.melspectrogram(y=data, sr=sample_rate).T, axis=0)
    result = np.hstack((result, mel))  # stacking horizontally

    return result

def extract_emotion(audio_path):
    data_, sample_rate_ = librosa.load(path_)
    X_ = np.array(extract_features(data_, sample_rate_))
    X_ = scaler.transform(X_.reshape(1,-1))
    pred_test_ = model.predict(np.expand_dims(X_, axis=2))
    y_pred_ = encoder.inverse_transform(pred_test_)
    # print("Pred test: \n", pred_test_)
    # print("categories:\n", encoder.categories_[0])

    # combine into a dictionary
    emotion_dict = dict(zip(encoder.categories_[0], pred_test_[0]))
    # print(emotion_dict)
    # sort emotions by confidence level
    sorted_emotion_dict = sorted(emotion_dict.items(), key=lambda x:x[1], reverse=True)
    # print(sorted_emotion_dict)

    # save top 3 detected emotions in an array together with their confidence score
    top3 = []
    top3.append((sorted_emotion_dict[0][0], "{:.2f}".format(sorted_emotion_dict[0][1]*100)))
    top3.append((sorted_emotion_dict[1][0], "{:.2f}".format(sorted_emotion_dict[1][1]*100)))
    top3.append((sorted_emotion_dict[2][0], "{:.2f}".format(sorted_emotion_dict[2][1]*100)))
    # print(top3)

    # print(y_pred_[0][0]) #emotion prediction
    # for value, emotion in zip(pred_test_[0], encoder.categories_[0]):
    #   print(emotion, f"{value:.10f}") #predicting values for each emotion

    return (top3)

path_ = r"C:\Users\Olan\Documents\Olan\3rd_year\2nd_semester\Software_Engineering_2\Prototype\project\scripts\emotion_detection\test_audios\.wav"
print(extract_emotion(path_))