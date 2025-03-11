from fastapi import APIRouter, WebSocket, UploadFile, File, Form
from service.ros import send_cmd_to_ros
from service.nlp import process_text
from service.speech import transcribe_audio
from pydantic import BaseModel
from config import ROSBRIDGE_WS_URL

router = APIRouter()

class CommandMsg (BaseModel):
    command: str

@router.get("/api/health/", tags=["Health"])
async def health_check():
    return { "status": "ok" }

# Test spacy NLP
@router.post("/api/text_command")
async def text_command(request: CommandMsg):
    processed_cmd = process_text(request.command)
    return {"Status": "Message sent", "Processed Command": processed_cmd}

# Process text command through Spacy NLP then send it to ros topic /linguistic_cmd
@router.post("/api/ros_text_command")
async def ros_text_command(request: CommandMsg):
    processed_cmd = process_text(request.command)
    return await send_cmd_to_ros(processed_cmd, ROSBRIDGE_WS_URL)

# Test OpenAI Whisper
@router.post("/api/voice_command")
async def voice_command(wav_file: UploadFile = File(...)):
    text_intent = await transcribe_audio(wav_file)
    processed_cmd = process_text(text_intent)
    return {"Status": "File sent", "Transcribed audio to text": text_intent, "Command": processed_cmd}

# Process audio WAV file through OpenAI Whisper to text command then process the text command through Spacy NLP then send it to ros topic /linguistic_cmd
@router.post("/api/ros_voice_command")
async def voice_command(wav_file: UploadFile = File(...)):
    text_intent = await transcribe_audio(wav_file)
    processed_cmd = process_text(text_intent)
    return await send_cmd_to_ros(processed_cmd, ROSBRIDGE_WS_URL)

