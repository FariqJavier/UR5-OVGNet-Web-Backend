import json
from fastapi import HTTPException
import websockets
import asyncio

async def send_cmd_to_ros(command: str, ros_url: str):
    message = {"op": "publish", "topic": "/linguistic_cmd", "msg": {"data": command}}
    try: 
        async with websockets.connect(ros_url) as websocket:
            await websocket.send(json.dumps(message))
            subscribe_msg = {"op": "subscribe", "topic": "/cmd_status"}
            await websocket.send(json.dumps(subscribe_msg))

            ### Get the message sent to /linguistic_cmd
            # try:
            #     response = await asyncio.wait_for(websocket.recv(), timeout=3)
            #     return {"Status": "Success", "Ros_Response": response}
            # except asyncio.TimeoutError:
            #     raise HTTPException(status_code=504, detail="No acknowledgment received from ROS")

            ### Get the acknowledgent status from /cmd_status
            while True:
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=3)
                    # return {"Status": "Success", "Ros_Response": response}
                    response_data = json.loads(response)
                    if response_data.get("topic") == "/cmd_status":
                        return {"Status": "Success", "Ros_Response": response_data["msg"]["data"]}
                except asyncio.TimeoutError:
                    raise HTTPException(status_code=504, detail="No acknowledgment received from ROS")
    except (websockets.exceptions.ConnectionClosedError, OSError):
        raise HTTPException(status_code=503, detail="Unable to connect to ROSBridge. Is it running?")
    except websockets.exceptions.InvalidURI:
        raise HTTPException(status_code=400, detail="Invalid ROSBridge WebSocket URL.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")