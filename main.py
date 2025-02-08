from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from typing import List
from src.ai_assistant import AI_Assistant

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

message_history = []

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    ai_asnt = AI_Assistant()

    try:
        while True:
            data = await websocket.receive_text()
            # await manager.send_message(f"Client {client_id}: {data}", websocket)
            print(f"Client {client_id}: {data}")
            message_history.append(f"{client_id} : {data}")
    
            await manager.broadcast(f"Client {client_id} says: {data}")
            
            # invoking the AI
            ai_response = ai_asnt.monitor_user_discussion(message_history=message_history, user_recent_message=data)
            if ai_response!= "skip":
                await manager.broadcast(f"AI says: {ai_response}")


    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client {client_id} disconnected")

@app.get("/", response_class=HTMLResponse)
async def get():
    with open("templates/index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)
