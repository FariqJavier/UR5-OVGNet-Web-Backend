import json
import websockets

ROSBRIDGE_WS_URL = "ws://localhost:9090"

async def send_to_ros(command: str):
    message = {"op": "publish", "topic": "/robot_command", "msg": {"data": command}}
    async with websockets.connect(ROSBRIDGE_WS_URL) as websocket:
        await websocket.send(json.dumps(message))
        response = await websocket.recv()
        return response
