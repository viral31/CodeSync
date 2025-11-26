from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from sqlalchemy.orm import Session
import json

from app.database import create_tables, get_db
from app.routers import rooms, autocomplete
from app.websocket_manager import manager
from app.services.room_service import RoomService
from app.middleware.exception_handler import (
    global_exception_handler,
    http_exception_handler,
    validation_exception_handler
)

app = FastAPI(title="CodeSync API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://*.vercel.app",
        "*"  # Remove this in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rooms.router)
app.include_router(autocomplete.router)

# Add exception handlers
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

@app.on_event("startup")
def startup_event():
    create_tables()

@app.websocket("/api/v1/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, db: Session = Depends(get_db)):
    await manager.connect(websocket, room_id)
    
    # Send current room code to new user
    room = RoomService.get_room(db, room_id)
    if room:
        await websocket.send_text(json.dumps({
            "type": "code_update",
            "code": room.code,
            "userId": "system"
        }))
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message["type"] == "code_update":
                # Update room code in database
                RoomService.update_room_code(db, room_id, message["code"])
                
                # Broadcast to other users in the room
                await manager.broadcast_to_room(room_id, message, websocket)
                
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)

@app.get("/")
def read_root():
    return {"message": "CodeSync API is running"}