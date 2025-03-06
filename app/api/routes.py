from fastapi import APIRouter, WebSocket, UploadFile, File, Form
from service.ros import send_to_ros
from service.nlp import process_text
from service.speech import transcribe_audio
from pydantic import BaseModel

router = APIRouter()

class CommandMsg (BaseModel):
    command: str

@router.get("/api/health/", tags=["Health"])
async def health_check():
    return { "status": "ok" }

@router.post("/api/text_command/")
async def text_command(request: CommandMsg):
    intent = process_text(request.command)
    return {"status": "Msg sent", "command": intent}
    # response = await send_to_ros(intent)
    # return {"status": "sent", "command": intent, "ros_response": response}

@router.post("/api/voice_command/")
async def voice_command(file: UploadFile = File(...)):
    text_command = await transcribe_audio(file)
    return await text_command(text_command)

@router.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
            response = await text_command(data)
            await websocket.send_json(response)
        except Exception as e:
            await websocket.send_json({"error": str(e)})
            break
