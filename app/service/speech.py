import whisper
from fastapi import UploadFile

model = whisper.load_model("base")

async def transcribe_audio(file: UploadFile) -> str:
    if not file or file.filename == "":
        raise ValueError("No audio file received")

    audio_bytes = await file.read()
    with open("temp_audio.wav", "wb") as f:
        f.write(audio_bytes)
    result = model.transcribe("temp_audio.wav")
    return result["text"]
