from project.scripts.transcribe import to_text

file_name = "harvard.wav"
transcribed = to_text(file_name, use_temp_folder=False)
print("output: ", transcribed)