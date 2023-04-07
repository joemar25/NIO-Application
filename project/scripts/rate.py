import os, librosa

__words_per_minute = 160

def estimate_speech_time(script):
    word_count = len(script.split())
    time_in_seconds = (word_count / __words_per_minute) * 60
    return time_in_seconds

def analyze_speech(audio, estimated_time):
    y, sr = librosa.load(audio)
    audio_duration = librosa.get_duration(y=y, sr=sr)

    if audio_duration < estimated_time * 0.9:
        label = "fast"
    elif audio_duration > estimated_time * 1.1:
        label = "slow"
    else:
        label = "ideal"
    
    score = 100 - abs(audio_duration - estimated_time) / max(audio_duration, estimated_time) * 100

    return {"score": score, "label": label}

def rate_score(audio, text, use_temp_folder=True, use_cloud_storage=False):
    
    if not (text and audio) or text == "no transcribed text.":
        return { "score": 0, "label": "" }
    
    temp_data_folder = ''
    if use_temp_folder and not use_cloud_storage:
        temp_data_folder = os.getcwd() + "/project/temp_data/"
        audio = temp_data_folder + audio
    
    # work work work
    speech_time = estimate_speech_time(text)
    score = analyze_speech(audio, speech_time)
    return score