import os
import whisper
import asyncio
import aiohttp
from functools import lru_cache

model = whisper.load_model('base')
result_cache = {}


@lru_cache(maxsize=128)
def transcribe_audio(audio_path):
    try:
        result = model.transcribe(
            audio_path,
            fp16=False,
            language='English',
            task='Translate'
        )
        readed_text = str(result.get("text", ""))
        return readed_text.strip() if readed_text else ""
    except Exception as e:
        # Handle exceptions appropriately
        ...


async def process_audio_async(audio_path):
    if audio_path in result_cache:
        return result_cache[audio_path]

    text = await asyncio.to_thread(transcribe_audio, audio_path)
    result_cache[audio_path] = text
    return text


def to_text(audio, use_temp_folder=True):
    # Check if audio has a value
    if not audio:
        return ""

    # Specify the path to the audio file
    if use_temp_folder:
        temp_data_folder = os.path.join(os.getcwd(), "project", "temp_data")
        audio_path = os.path.join(temp_data_folder, audio)
    else:
        audio_path = audio

    # Check if the audio file exists
    if not os.path.exists(audio_path):
        return ""

    # Check if the transcription is already cached
    if audio_path in result_cache:
        return result_cache[audio_path]

    # Process the audio file asynchronously
    async def fetch_audio():
        async with aiohttp.ClientSession() as session:
            return await process_audio_async(audio_path)

    text = asyncio.run(fetch_audio())
    return text
