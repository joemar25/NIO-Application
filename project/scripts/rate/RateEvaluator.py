"""
This module provides functionality for analyzing the duration of an audio recording and comparing it with the expected speech time based on a provided transcript. The module uses the librosa library for audio processing.

Functions:
- estimate_speech_time(script): Estimates the speech time (in seconds) based on the number of words in the provided transcript.
- analyze_speech(audio, estimated_time): Analyzes the duration of the provided audio file and compares it with the estimated speech time to determine whether the speech is too fast, too slow, or ideal.
- rate_score(audio, text, use_temp_folder=True): Computes a score (out of 100) and a label for the provided audio and transcript based on the analysis performed by analyze_speech().

Constants:
- __words_per_minute: The average number of words a person can speak in one minute.

Dependencies:
- librosa

Note: This rate is inspired from the website 'https://www.thevoicerealm.com/count-script.php' for estimating the scripts duration
      - https://www.calculateme.com/time/hours-minutes-seconds/to-seconds/
      - https://clearly-speaking.com/what-is-the-ideal-rate-of-speech/
"""

import os, librosa

class Rate:
    """
    The `Rate` class provides functionality for estimating the duration of a speech given a transcript, 
    and then comparing the estimated duration to the actual duration of an audio file. 
    """

    __words_per_minute = 160

    @staticmethod
    def estimate_speech_time(script: str) -> float:
        """
        This method estimates the duration of a speech given its transcript.

        Args:
            script (str): The transcript of the speech.

        Returns:
            float: The estimated duration of the speech in seconds.
        """
        word_count = len(script.split())
        time_in_seconds = (word_count / Rate.__words_per_minute) * 60
        return time_in_seconds

    @staticmethod
    def analyze_speech(audio: str, estimated_time: float) -> dict:
        """
        This method compares the estimated duration of a speech to the actual duration of an audio file, 
        and returns a dictionary with a score and label indicating how closely they match.

        Args:
            audio (str): The file path to the audio file.
            estimated_time (float): The estimated duration of the speech.

        Returns:
            dict: A dictionary with a score and label indicating how closely the estimated and actual 
                  durations match.
        """
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

    @staticmethod
    def rate_score(audio: str, text: str, use_temp_folder: bool = True) -> dict:
        """
        This method estimates the duration of a speech based on its transcript, compares it to the actual duration
        of an audio file, and returns a score and label indicating how closely they match.

        Args:
            audio (str): The file path to the audio file.
            text (str): The transcript of the speech.
            use_temp_folder (bool): A flag indicating whether or not to use a temporary data folder. Defaults to True.

        Returns:
            dict: A dictionary with a score and label indicating how closely the estimated and actual durations match.
        """
        if not (text and audio) or text == "no transcribed text.":
            return {"score": 0, "label": ""}

        temp_data_folder = ''
        if use_temp_folder:
            temp_data_folder = os.path.join(os.getcwd(), "project", "temp_data")
            audio = os.path.join(temp_data_folder, audio)

        # Estimate speech time and analyze speech
        speech_time = Rate.estimate_speech_time(text)
        score = Rate.analyze_speech(audio, speech_time)

        return score
