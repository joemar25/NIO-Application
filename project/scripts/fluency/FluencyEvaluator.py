# Steps to prepare the audio file and run the program:
# Before running the program, please ensure:
# 1. You have installed the "my-voice-analysis" package.
# 2. You have placed the "myspsolution.praat" file in the directory of the audio files to be tested.
# 3. The audio file has been converted to 44kHz sample rate.

# Program workflow:
# 1. Check if the audio is already in 44kHz sample rate. If not, convert it.
# 2. Count the number of filler words and pauses in the audio file using "myspsolution.praat".
# 3. (Optional) Generate a TextGrid file to visualize the analysis in Praat.

import os, wave, parselmouth, tempfile
from parselmouth.praat import run_file

class FluencyEvaluator:
    def __init__(self):
        self.script_path = os.getcwd() + "/project/scripts/fluency/myspsolution.praat"
        self._output_cache = {}

    def _extract_fluency_score(self, output):
        if isinstance(output, bytes):
            output = output.decode("utf-8")
        filler_count = output.strip().split()[1]
        return int(filler_count)

    def _calculate_duration(self, audio_file_path):
        with wave.open(audio_file_path) as wav_file:
            return wav_file.getnframes() / wav_file.getframerate()

    def _run_praat_script(self, audio_file_path):
        if audio_file_path in self._output_cache:
            return self._output_cache[audio_file_path]
        
        with tempfile.TemporaryDirectory() as tmp_dir:
            try:
                objects = run_file(
                    self.script_path,
                    -20, 2, 0.3, "yes",
                    audio_file_path, tmp_dir,
                    80, 400, 0.01,
                    capture_output=True
                )
                self._output_cache[audio_file_path] = objects[1]
                return objects[1]
            except Exception as e:
                # raise Exception("Failed to run Praat script: " + str(e))
                ...

    def filler_score(self, audio_file_path):
        output = self._run_praat_script(audio_file_path)
        fill_pause_num = self._extract_fluency_score(output)

        duration_seconds = self._calculate_duration(audio_file_path)
        fluency_score = abs(100 - (duration_seconds - fill_pause_num))
        return fluency_score
    
    def count_fillers(self, audio_file_path):
        output = self._run_praat_script(audio_file_path)
        fill_count = self._extract_fluency_score(output)
        return fill_count
