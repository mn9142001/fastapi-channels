from fastapi import FastAPI, WebSocket, Request
from channels import FastSocket
import json

app = FastAPI()


@app.get('/login')
async def LogIn(request : Request):
    await FastSocket.group_send("group-1", json.dumps({"message" : "calling from login"}))

@app.websocket("/{id}")
async def websocket_endpoint(websocket: WebSocket, id):
    name:str = f"group-{id}"
    await FastSocket.group_add(name, websocket)
    